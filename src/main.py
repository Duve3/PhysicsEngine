"""
main.py

Contains the main point of the game
"""
import pygame
import ui
import physics
import sys
import os

DEFAULT_FONT_LOC = f"{os.path.dirname(sys.argv[0])}/assets/Comfortaa.ttf"  # WARN: Possibly worse than what I was doing before but I am NOT setting up a config file for this!!!


class MainMenu:
    def __init__(self, screen: ui.CScreen):
        self.screen: ui.CScreen = screen

        self.FONT_default = ui.CUIFont(DEFAULT_FONT_LOC, 20, ui.CUColor.BLACK())

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


class BoxDraggable(ui.CUIButton):
    def __init__(self, x: float, y: float, width: float, height: float, color: ui.CUColor):
        super().__init__(x, y, width, height, color)
        self.registeredEvents = [pygame.MOUSEBUTTONUP, pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION]

        self.hasDrawn = True  # WARN: not the best idea, but we threw optimizations far out of the window years ago

        self.BOX_renderable = physics.Box(x, y, width, height, color, 1, 0, 0)

    def draw(self, surface: pygame.Surface):
        self.BOX_renderable.color = self.color
        self.BOX_renderable.draw(surface)

    def tick(self, event: pygame.Event, mouse_pos: tuple[int, int]):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.color = self.pressedColor
                self.isPressed = True

            else:
                self.color = self.defaultColor
                self.isPressed = False

            return

        if event.type == pygame.MOUSEBUTTONUP:
            self.color = self.defaultColor
            self.isPressed = False

            return

        if event.type == pygame.MOUSEMOTION:
            if self.collidepoint(mouse_pos[0], mouse_pos[1]):
                self.color = self.highlightColor
                self.isHovered = True

            else:
                self.color = self.defaultColor
                self.isHovered = False

            return


class BottomScrollbar:
    """
    This will be like our 'toolbox' that contains stuff we can use
    """

    def __init__(self, screen: ui.CScreen, game_ref: 'Game'):
        self.screen = screen
        height = 200
        self.game_ref: 'Game' = game_ref

        self.RECT_drawable = ui.CRect(0, screen.surface.height - height, screen.surface.width, height,
                                      ui.CUColor.GRAY())

        self.BOX_DRAGGABLE = BoxDraggable(self.RECT_drawable.x + 20, self.RECT_drawable.y + 100, 100, 100,
                                          ui.CUColor.RED())

        self.MANAGER_ui = ui.CUIManager([self.BOX_DRAGGABLE])

        self.summoned: physics.PhysicsObject = None  # noqa ; probably fineeee

    def draw(self):
        self.screen.draw(self.RECT_drawable)
        self.BOX_DRAGGABLE.draw(self.screen.surface)

        if self.summoned:
            self.summoned.draw(self.screen.surface)

    def tick(self, events):
        self.MANAGER_ui.tick(events)
        mp = pygame.mouse.get_pos()
        mp = [mp[0], mp[1]]

        if self.BOX_DRAGGABLE.isPressed:
            if not self.summoned:
                self.summoned = physics.Box(mp[0], mp[1], 50, 50, ui.CUColor.RED(), 2, 0, 0)

            self.summoned.x, self.summoned.y = mp[0] - self.summoned.width//2, mp[1] - self.summoned.height//2

        else:
            if self.summoned:
                self.game_ref.MANAGER_physics.add(self.summoned)
                self.summoned = None


class Game:
    def __init__(self, screen: ui.CScreen):
        self.screen = screen

        self.BOX_box = physics.Box(100, 0, 50, 50, ui.CUColor.RED())
        self.SCROLLBAR_bottom = BottomScrollbar(screen, self)
        self.FLOAT_ground = self.SCROLLBAR_bottom.RECT_drawable.y
        print(self.FLOAT_ground)

        # absolutely DISGUSTING line of code, has like three inline things that just shouldn't be done inline... ; edit: no more lambda!!!! yippie
        self.BUTTON_force = ui.CUITextButton(100, 100, 200, 50, ui.CUColor.BLUE().darken(20, retColor=True),
                                             ui.CUIFont(DEFAULT_FONT_LOC, 20, ui.CUColor.WHITE()), "magic button",
                                             onPress=self.BUTTON_force_onPress)

        self.MANAGER_physics = physics.PhysicsManager([self.BOX_box])
        self.MANAGER_ui = ui.CUIManager([self.BUTTON_force])

    def BUTTON_force_onPress(self):
        self.MANAGER_physics.apply_accel_to_all_objs((10, 100))

    def run(self):
        while True:
            dt = self.screen.tick() / 1000

            events = pygame.event.get()
            self.MANAGER_ui.tick(events)
            self.SCROLLBAR_bottom.tick(events)
            self.MANAGER_physics.tick(int(self.FLOAT_ground),
                                      dt)  # typecast to int ; might lose data, but I think we're fine.

            for event in events:
                if event.type == pygame.QUIT:
                    self.screen.close(kill=True)

            self.screen.fill(ui.CUColor.BLACK())

            self.SCROLLBAR_bottom.draw()
            self.MANAGER_physics.draw(self.screen.surface)
            self.BUTTON_force.draw(self.screen.surface)

            pygame.display.flip()


def main():
    ui.init()

    screen = ui.CScreen((800, 800), caption="Pygame Physics Engine", clock=True, fps=60)

    main_menu = MainMenu(screen)
    game = Game(screen)

    main_menu.run()
    game.run()


if __name__ == '__main__':
    main()
