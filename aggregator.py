#!/usr/bin/env python3

from babel.dates import format_date, format_datetime
from datetime import datetime, date
from html2text import HTML2Text
from textwrap import shorten
from typing import Dict, List
import sys
import jinja2
import json

from digitaluni import DigitalUniView


def parse_end_date(homework: Dict) -> date:
    FMT = "%Y-%m-%d"
    return datetime.strptime(homework["activite_date_fin"], FMT).date()


def text_output(homework_list: List[Dict]) -> None:
    html_renderer = HTML2Text()
    homework_list.sort(key=parse_end_date)

    for hm in homework_list:
        name = hm["activite_nom"]
        # human readable date
        end_date = format_date(parse_end_date(hm), format="full", locale="fr")
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


def html_output(homework_list: List[Dict], out_file: str) -> None:
    homework_list.sort(key=parse_end_date)

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader("templates"),
    )
    env.filters.update({
        "format_datetime": format_datetime,
        "format_date": format_date,
        "parse_end_date": parse_end_date,
    })

    template = env.get_template("html_output.jinja2")
    template_values = {
        "now": datetime.now(),
    }

    with open(out_file, "w") as f:
        f.write(template.render(homework_list=homework_list, **template_values))


if __name__ == "__main__":
    #  with DigitalUniView() as view:
        #  view.connect("credentials.yml")
        #  view.discover_homework()
        #  raw = view.homework
        #  text_output(raw)
    with open("dump.json") as f:
        raw = json.load(f)
    html_output(raw, sys.argv[1])
    # TODO: don't forget to remove the dump
