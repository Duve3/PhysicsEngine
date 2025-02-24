"""
main.py

Contains the main point of the game
"""
import ui
import os
from settings import Settings
from mainMenu import MainMenu
from game import Game


def define_settings_defaults(settings: Settings):
    if not os.path.isfile(settings.assets_dir + "\\Comfortaa.ttf"):
        raise FileNotFoundError("Missing Critical Asset: Comfortaa.ttf! Failed to launch!")

    settings.FONTLOC_comfortaa = settings.assets_dir + "\\Comfortaa.ttf"


def main():
    ui.init()

    screen = ui.CScreen((1000, 800), caption="Pygame Physics Engine", clock=True, fps=60)
    settings = Settings()

    # Asset Declarations (Maybe move this to the settings file?)
    define_settings_defaults(settings)

    main_menu = MainMenu(screen, settings)
    game = Game(screen, settings)

    main_menu.run()
    game.run()


if __name__ == '__main__':
    main()
