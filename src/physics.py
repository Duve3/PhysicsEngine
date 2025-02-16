"""
physics.py

Contains all physics-based stuff, like objects, math eqs, and more
"""
from argparse import ArgumentError
from typing import Sequence
import ui
import pygame


# TODO: i think there are some flaws in the grounded system,
#       Example: like if you want to move an object again after it hits the ground, it cant?
#       I think we should allow movements to continue, just set accel's and vel's to 0
#       No form of stoppage via variables

class Hitbox(pygame.FRect):
    def __init__(self, x, y, w, h):
        super().__init__([x, y, w, h])


class PhysicsObject:
    def __init__(self, x, y, width, height, color: ui.CUColor, hitbox: Hitbox, mass: float = 1.0, velx: int = 0, vely: int = 0):
        if mass <= 0:
            raise ArgumentError(None, "Mass cannot be less than 0 (causes UB)")

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.velx = velx
        self.vely = vely
        self.accelx = 0
        self.accely = 0
        self.grounded_y = False
        self.grounded_x = False  # debug: this is the stuff i was talking about in my to\do
        self.hitbox = hitbox
        self.mass = mass

    def tick(self, dt: float):
        self.x += self.velx * dt
        self.y += self.vely * dt

        self.velx += self.accelx * dt
        self.vely += self.accely * dt

        self.hitbox.x = self.x
        self.hitbox.y = self.y

    def next_frame(self, dt: float) -> list[float]:
        x: float = self.x + self.velx * dt
        y: float = self.y + self.vely * dt
        return [x, y]

    def disable_physics(self):
        self.velx = 0
        self.vely = 0
        self.accelx = 0
        self.accely = 0
        self.grounded_y = True

    def apply_force(self, force: Sequence[int]):
        if not self.grounded_y:
            self.accely += force[1] / self.mass

        self.accelx += force[0] / self.mass

    def apply_accel(self, accel: Sequence[int]):
        if not self.grounded_y:
            self.accely += accel[1]

        self.accelx += accel[0]

    def draw(self, surface: pygame.Surface):
        # to override
        raise NotImplementedError("The `DRAW` Method should be overridden by subclasses!")


class Box(PhysicsObject):
    def __init__(self, x, y, width, height, color: ui.CUColor, mass: float = 1, velx: int = 0, vely: int = 0):
        super().__init__(x, y, width, height, color, Hitbox(x, y, width, height), mass, velx, vely)

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, self.color.darken(60), (self.x, self.y, self.width, self.height), width=5)


class PhysicsManager:
    """
    Makes handling all the objects on screen easier
    """

    def __init__(self, objects: list[PhysicsObject]):
        self.objs = objects

    def tick(self, ground: int, left_edge: int, right_edge: int, deltatime: float):
        for obj in self.objs:
            obj.tick(deltatime)

            if obj.grounded_y is True:
                continue

            # REST OF THIS LOOP IS ONLY FOR OBJECTS THAT AREN'T GROUNDED

            nextframe_x, nextframe_y = obj.next_frame(deltatime)

            if nextframe_y >= ground - obj.height:
                obj.y = ground - obj.height
                obj.vely = 0
                obj.accely = 0
                obj.grounded_y = True

            if nextframe_x <= left_edge:
                obj.x = left_edge
                obj.velx = 0
                obj.accelx = 0
                obj.grounded_x = True

            # COLLISION BETWEEN OBJS

            for o2 in self.objs:
                if o2 == obj:
                    continue

                if obj.hitbox.colliderect(o2.hitbox):
                    obj.y = o2.y - obj.height
                    obj.vely = 0
                    obj.accely = 0
                    obj.grounded_y = True

    def add(self, obj: PhysicsObject):
        self.objs.append(obj)

    def remove(self, obj: PhysicsObject):
        self.objs.remove(obj)

    def apply_force_to_all_objs(self, force: Sequence[int]):
        for obj in self.objs:
            obj.apply_force(force)

    def apply_accel_to_all_objs(self, accel: Sequence[int]):
        for obj in self.objs:
            obj.apply_accel(accel)

    def draw(self, surface: pygame.Surface):
        for obj in self.objs:
            obj.draw(surface)
