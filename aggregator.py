from datetime import datetime
from html2text import HTML2Text
from textwrap import shorten
from typing import Dict, List
import json

from digitaluni import DigitalUniView


def end_datetime(homework: Dict) -> datetime:
    FMT = "%Y-%m-%d"
    return datetime.strptime(homework["activite_date_fin"], FMT)


def text_output(homework_list: List[Dict]) -> None:
    html_renderer = HTML2Text()
    homework_list.sort(key=end_datetime)

    for hm in homework_list:
        name = hm["activite_nom"]
        end_date = hm["activite_date_fin"]
        sequence_name = hm["_aggregatorinfo_sequence"]["name"]
        ue_url = hm["_aggregatorinfo_sequence"]["ue_url"]
        description = shorten(
            html_renderer.handle(hm["activite_description"]),
            width=130,
        )

        print(f"- avant le {end_date} pour {sequence_name}")
        print(f"\tLien vers l'{sequence_name[:4]} : {ue_url}")
        print(f"\t{name}")
        print(f"\t{description}")
        print()


if __name__ == "__main__":
    with DigitalUniView() as view:
        view.connect("credentials.yml")
        view.discover_homework()
        raw = view.homework
        text_output(raw)
    # TODO: don't forget to remove the dump
    #  with open("dump.json") as f:
        #  raw = json.load(f)
    #  text_output(raw)
