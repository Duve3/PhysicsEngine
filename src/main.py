"""
main.py

Contains the main point of the game
"""
import pygame
import ui  # THE GOATTTTTT (LEBROOOOOOOOOONNNN)


class MainMenu:
    def __init__(self, screen: ui.CScreen):
        self.screen: ui.CScreen = screen

        # WARN: This is BAD practice, using hardcoded font values is a terrible idea but i dont care rn
        self.FONT_default = ui.CUIFont("./assets/Comfortaa.ttf", 20, ui.CUColor.BLACK())

        self.BUTTON_play = ui.CUITextButton(100, 100, 100, 50, ui.CUColor.GREEN(), font=self.FONT_default, text="Play", onPress=self.exit)
        self.MANAGER_ui = ui.CUIManager([self.BUTTON_play])
        self.loop = True

    def run(self):
        while self.loop:
            events = pygame.event.get()
            self.MANAGER_ui.tick(events)
            for event in events:
                if event.type == pygame.QUIT:
                    self.screen.close(kill=True)

            self.screen.fill(ui.CUColor.CYAN())

            self.BUTTON_play.draw(self.screen.surface)

            pygame.display.flip()

    def exit(self):
        self.loop = False


class Game:
    def __init__(self, screen: ui.CScreen):
        self.screen = screen

        self.MANAGER_ui = ui.CUIManager([])

    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.screen.close(kill=True)

            self.screen.fill(ui.CUColor.BLACK())

            pygame.display.flip()


def main():
    ui.init()

    screen = ui.CScreen((800, 600), caption="Pygame Physics Engine", clock=True, fps=60)

    main_menu = MainMenu(screen)
    game = Game(screen)

    main_menu.run()
    game.run()


if __name__ == '__main__':
    main()
