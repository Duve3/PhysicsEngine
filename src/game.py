import ui
import pygame
import physics
from settings import Settings
from scrollbars import BottomScrollbar, DataSidebar


class Game:
    def __init__(self, screen: ui.CScreen, settings: Settings):
        self.screen = screen

        self.BOX_box = physics.Box(100, 0, 50, 50, ui.CUColor.RED())
        self.SCROLLBAR_bottom = BottomScrollbar(screen, self)
        self.FLOAT_ground = self.SCROLLBAR_bottom.RECT_drawable.y
        print(self.FLOAT_ground)

        self.BUTTON_force = ui.CUITextButton(100, 100, 200, 50, ui.CUColor.BLUE().darken(20, retColor=True),
                                             ui.CUIFont(settings.FONTLOC_comfortaa, 20, ui.CUColor.WHITE()), "magic button",
                                             onPress=self.BUTTON_force_onPress)

        self.MANAGER_physics = physics.PhysicsManager([self.BOX_box])
        self.MANAGER_ui = ui.CUIManager([self.BUTTON_force])

    def BUTTON_force_onPress(self):
        self.MANAGER_physics.apply_accel_to_all_objs((100, 100))

    def run(self):
        while True:
            dt = self.screen.tick() / 1000

            events = pygame.event.get()
            self.MANAGER_ui.tick(events)
            self.SCROLLBAR_bottom.tick(events)
            self.MANAGER_physics.tick(int(self.FLOAT_ground),
                                      0, self.screen.surface.width,
                                      dt)  # typecast to int ; might lose data, but I think we're fine.

            for event in events:
                if event.type == pygame.QUIT:
                    self.screen.close(kill=True)

            self.screen.fill(ui.CUColor.BLACK())

            self.SCROLLBAR_bottom.draw()
            self.MANAGER_physics.draw(self.screen.surface)
            self.BUTTON_force.draw(self.screen.surface)

            pygame.display.flip()
