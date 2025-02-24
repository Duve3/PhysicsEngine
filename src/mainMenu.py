import ui
import pygame
from settings import Settings


class MainMenu:
    def __init__(self, screen: ui.CScreen, settings: Settings):
        self.screen: ui.CScreen = screen

        self.FONT_default = ui.CUIFont(settings.FONTLOC_comfortaa, 20, ui.CUColor.BLACK())

        self.BUTTON_play = ui.CUITextButton(100, 100, 100, 50, ui.CUColor.GREEN(), font=self.FONT_default, text="Play",
                                            onPress=self.exit)
        self.BUTTON_play.align_center(self.screen.surface, 0, 0)
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
