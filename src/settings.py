"""
settings.py
handles the location and usage of settings and asset objects
"""

from pathlib import Path
import os
import json
import copy


def find_file(name: str, lim: int = 5, directory_mode: bool = False) -> str:
    """
    Finds a file by moving upwards in the file tree
    ^ WARN: this does NOT go into folders it finds while moving upwards!
    :param str name: Name of the file
    :param int lim: Limit of how high to search, defaults to 5
    :param bool directory_mode: Whether to also search for a directory of this name, defaults to False
    :return str: the File path
    """
    dots = "."
    while True:
        print(f"trying {dots}/{name}")  # DEBUG
        if os.path.isfile(f"{dots}/{name}"):
            return str(Path(f"{dots}/{name}").absolute())  # converting these dot paths into absolute values.

        if directory_mode and os.path.isdir(f"{dots}/{name}"):
            return str(Path(f"{dots}/{name}").absolute())  # converting these dot paths into absolute values.

        if len(dots) > lim:  # prevents repeating infinitely for a file (also prevents finding a file that is way off)
            raise FileNotFoundError(f"Failed to find {'directory' if directory_mode else 'file'}: {name}!")

        dots += "."


class Settings:
    """
    A wrapper around the settings.json object
    """
    TEMPLATE = {
        "assets_dir": str | None
    }

    def __init__(self):
        self.path = find_file("settings.json")

        if self.path is None:
            with open("./settings.json", "w") as sf:
                sf.write(json.dumps(self.TEMPLATE))
                self.path = find_file("settings.json")

        # data values
        self.assets_dir = str | None

        # set later values (set in main.py)
        self.FONTLOC_comfortaa = str | None

        self.read()

        if self.assets_dir is None:
            self.assets_dir = find_file("assets", directory_mode=True)
            self.write()

    def read(self):
        with open(self.path, 'r') as sf:
            d = sf.read()

            nd = json.loads(d)

            self.assets_dir = nd.get("assets_dir", None)

    def write(self):
        with open(self.path, 'w') as sf:
            d = copy.deepcopy(self.TEMPLATE)

            d["assets_dir"] = self.assets_dir

            nd = json.dumps(d)

            sf.write(nd)
