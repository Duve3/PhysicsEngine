"""
physics.py

Contains all physics-based stuff, like objects, math eqs, and more
"""
from typing import Sequence
import ui
import pygame


class PhysicsObject:
    def __init__(self, x, y, width, height, color: ui.CUColor, velx: int = 0, vely: int = 0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.velx = velx
        self.vely = vely
        self.accelx = 0
        self.accely = 0
        self.grounded = False

    def tick(self, dt: float):
        self.x += self.velx * dt
        self.y += self.vely * dt

        self.velx += self.accelx * dt
        self.vely += self.accely * dt


class Box(PhysicsObject):
    def __init__(self, x, y, width, height, color: ui.CUColor, velx: int = 0, vely: int = 0):
        super().__init__(x, y, width, height, color, velx, vely)

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(surface, self.color.darken(60), (self.x, self.y, self.width, self.height), width=5)


class PhysicsManager:
    """
    Makes handling all the objects on screen easier
    """
    def __init__(self, objects: list[PhysicsObject]):
        self.objs = objects

    def tick(self, ground: int, deltatime: float):
        for obj in self.objs:
            obj.tick(deltatime)

            nextframe_y = obj.y + obj.vely * deltatime

            if nextframe_y >= ground - obj.height and obj.grounded is False:
                obj.y = ground - obj.height
                obj.vely = 0
                obj.accely = 0
                obj.grounded = True

    def add(self, obj: PhysicsObject):
        self.objs.append(obj)

    def remove(self, obj: PhysicsObject):
        self.objs.remove(obj)

    def apply_force(self, force: Sequence[int]):
        for obj in self.objs:
            obj.accelx += force[0]
            obj.accely += force[1]
