from bs4 import BeautifulSoup
from typing import List, Dict
import requests
import sys
import yaml
import json

WANTED_INFO = [
    "activite_nom",
    #  "activite_description",
    "activite_date_debut",
    "activite_heure_debut",
    "activite_date_fin",
    "activite_heure_fin",
    "activite_duree_contractuelle",
]


# list of "seminaire_i_id" for each UE
UE_LIST = [
    {"id": 12865, "name": "UE 31 - Activité, cognition"},
    {
        "id": 12866,
        "name": "UE 32 - Technologies Numériques et Apprentissage tout au long de la vie",
    },
    {
        "id": 12867,
        "name": "UE 33 - Développement Informatique, Réseaux et Systèmes Complexes",
    },
    {"id": 12868, "name": "UE 34 - Conception des applications numériques immersives"},
]


def get_sequence_ids(session: requests.Session, seminaire_id: int) -> List[int]:
    """Get the sequence ids of every course in the UE represented by seminaire_id"""

    sequences = session.get(
        f"https://campus.sfc.unistra.fr/rest/sequences/idSemI/{seminaire_id}"
    ).json()

    return [seq["sequence_id"] for seq in sequences]


def get_homework_list(
    session: requests.Session, seminaire_id: int, sequence_id: int
) -> List[Dict]:
    """Get the list of homework for the course represented by sequence_id"""

    activities = session.get(
        f"https://campus.sfc.unistra.fr/rest/activities/idSeq/{sequence_id}/utilId/13530/idSemI/{seminaire_id}"
    ).json()

    return filter_homework(activities)


def get_credentials():
    with open("credentials.yml") as f:
        try:
            credentials = yaml.safe_load(f)
        except yaml.YAMLError:
            print(
                "Le fichier credentials.yml n'est pas valide, l'erreur complète est :",
                file=sys.stderr,
            )
            raise

    return credentials


def filter_homework_information(activity: Dict):
    return {k: v for k, v in activity.items() if k in WANTED_INFO}


def filter_homework(activities: List[Dict]):
    return [
        filter_homework_information(act)
        for act in activities
        if act["activite_est_validation"] == "1"
    ]


if __name__ == "__main__":
    credentials = get_credentials()

    with requests.Session() as session:
        session.post("https://campus.sfc.unistra.fr/login", data=credentials)

        all_homework = []
        for ue in UE_LIST:
            for sequence in get_sequence_ids(session, ue["id"]):
                all_homework.extend(get_homework_list(session, ue["id"], sequence))

        print(json.dumps(all_homework, sort_keys=True, indent=4))
