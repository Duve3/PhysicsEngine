import ui
import pygame
import physics
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.game import Game


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

        self.summoned: physics.PhysicsObject = None

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

            self.summoned.x, self.summoned.y = mp[0] - self.summoned.width // 2, mp[1] - self.summoned.height // 2

        else:
            if self.summoned:
                self.game_ref.MANAGER_physics.add(self.summoned)
                self.summoned = None


class DataSidebar:
    def __init__(self, screen: ui.CScreen, game_ref: 'Game'):
        self.screen = screen
        height = 200
        self.game_ref: 'Game' = game_ref

        self.RECT_drawable = ui.CRect(0, screen.surface.height - height, screen.surface.width, height,
                                      ui.CUColor.GRAY())

        self.MANAGER_ui = ui.CUIManager([])

    def draw(self):
        self.screen.draw(self.RECT_drawable)

    def tick(self, events):
        self.MANAGER_ui.tick(events)
