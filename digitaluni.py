from __future__ import annotations
from bs4 import BeautifulSoup
from dataclasses import dataclass, asdict
from typing import List, Dict
import requests
import sys
import yaml


@dataclass
class UE:
    seminaire_id: int
    name: str


@dataclass
class UESequence:
    sequence_id: int
    name: str
    ue: UE
    ue_url: str

    @property
    def shortname(self):
        return self.name.split()[0]


class DigitalUniView:
    ue_list: List[UE]
    sequences: List[UESequence]
    session: requests.Session
    homework: List[Dict]

    def __init__(self) -> None:
        self.session = requests.Session()

    def __enter__(self) -> DigitalUniView:
        # No idea if storing the result of __enter__() is really needed
        self._session_ctx_mngr = self.session.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, tb) -> None:
        self.session.__exit__(exc_type, exc_value, tb)

    def connect(self, cred_path: str) -> None:
        """Log into digitaluni using credentials from the `cred_path` file"""
        with open(cred_path) as f:
            try:
                credentials = yaml.safe_load(f)
            except yaml.YAMLError:
                print(
                    f"Le fichier {cred_path} n'est pas valide, l'erreur complète est :",
                    file=sys.stderr,
                )
                raise

        self.session.post("https://campus.sfc.unistra.fr/login", data=credentials)

    def _discover_ues(self) -> None:
        """Build self.ue_list by looking at available UEs on the landing page

        This function should not be called directly, it is used by
        `_discover_sequences`
        """
        landing_page = BeautifulSoup(
            self.session.get("https://campus.sfc.unistra.fr/").text, "html.parser"
        )
        html_list = landing_page.select_one("ul#color-menuJ.dl-submenu")
        if not html_list:
            raise RuntimeError(
                "Impossible de trouver la liste des UE sur digitaluni "
                "(peut être que l'ID ou la classe de l'élément HTML a changé)"
            )
        html_ue_links = html_list.find_all("a")

        self.ue_list = []
        for ue_link in html_ue_links:
            # skip "Informations générales, not a real UE
            if ue_link.text.startswith("Informations"):
                continue

            self.ue_list.append(
                UE(seminaire_id=int(ue_link["href"].split("/")[-1]), name=ue_link.text)
            )

    def _discover_sequences(self) -> None:
        """Build the self.sequences list by looking at available sequences in each UE

        This function should not be called directly, it is used by
        `discover_homework`
        """
        self._discover_ues()
        self.sequences = []
        for ue in self.ue_list:
            json_sequence_list = self.session.get(
                f"https://campus.sfc.unistra.fr/rest/sequences/idSemI/{ue.seminaire_id}"
            ).json()

            for seq in json_sequence_list:
                self.sequences.append(
                    UESequence(
                        sequence_id=seq["sequence_id"],
                        name=seq["sequence_nom"],
                        ue=ue,
                        ue_url=f"https://campus.sfc.unistra.fr/progressionpedago/cours/idSemI/{ue.seminaire_id}/seqId/{seq['sequence_id']}/#/cours",
                    )
                )

    def discover_homework(self) -> None:
        """Build the self.homework list by looking at available activities in each sequence"""
        self._discover_sequences()
        self.homework = []
        for seq in self.sequences:
            activities = self.session.get(
                f"https://campus.sfc.unistra.fr/rest/activities/idSeq/{seq.sequence_id}/utilId/13530/idSemI/{seq.ue.seminaire_id}"
            ).json()

            for act in activities:
                # Homework activities are marked with "activite_est_validation" on digitaluni
                if act["activite_est_validation"] == "1":
                    # Add a reference to the parent sequence in the activity
                    # information, this allows displayers to link each activity
                    # to the sequence or UE information
                    act["_aggregatorinfo_sequence"] = asdict(seq)
                    self.homework.append(act)
