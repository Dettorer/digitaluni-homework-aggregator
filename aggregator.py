import json

from digitaluni import DigitalUniView


if __name__ == "__main__":
    with DigitalUniView() as view:
        view.connect("credentials.yml")
        view.discover_homework()

        print("---------")
        print(view.ue_list)
        print("---------")
        print(view.sequences)
        print("---------")
        print(json.dumps(view.homework, indent=4))
