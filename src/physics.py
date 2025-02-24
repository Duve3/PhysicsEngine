"""
physics.py

Contains all physics-based stuff, like objects, math eqs, and more
"""
from argparse import ArgumentError
from typing import Sequence
import ui
import pygame


# TODO: Add a way to use assets instead of rectangles when drawing objects


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

    def apply_force(self, force: Sequence[int]):
        self.accely += force[1] / self.mass

        self.accelx += force[0] / self.mass

    def apply_accel(self, accel: Sequence[int]):
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

            nextframe_x, nextframe_y = obj.next_frame(deltatime)

            if nextframe_y >= ground - obj.height:
                obj.y = ground - obj.height
                obj.vely = 0
                obj.accely = 0

            if nextframe_x <= left_edge:
                obj.x = left_edge
                obj.velx = 0
                obj.accelx = 0

            if nextframe_x >= right_edge - obj.width:
                obj.x = right_edge - obj.width
                obj.velx = 0
                obj.accelx = 0

            # COLLISION BETWEEN OBJS

            for o2 in self.objs:
                if o2 == obj:
                    continue

                if obj.hitbox.colliderect(o2.hitbox):
                    obj.y = o2.y - obj.height
                    obj.vely = 0
                    obj.accely = 0

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
