"""
physics.py

Contains all physics-based stuff, like objects, math eqs, and more
"""
from typing import Sequence, overload
import ui
import pygame


class Hitbox(pygame.FRect):
    def __init__(self, x, y, w, h):
        super().__init__([x, y, w, h])


class PhysicsObject:
    def __init__(self, x, y, width, height, color: ui.CUColor, hitbox: Hitbox, velx: int = 0, vely: int = 0):
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
        self.hitbox = hitbox

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
        self.grounded = True

    def draw(self, surface: pygame.Surface):
        # to override
        pass


class Box(PhysicsObject):
    def __init__(self, x, y, width, height, color: ui.CUColor, velx: int = 0, vely: int = 0):
        super().__init__(x, y, width, height, color, Hitbox(x, y, width, height), velx, vely)

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

            if obj.grounded is True:
                continue

            # REST OF THIS LOOP IS ONLY FOR OBJECTS THAT AREN'T GROUNDED

            nextframe_y, nextframe_x = obj.next_frame(deltatime)

            if nextframe_y >= ground - obj.height:
                obj.y = ground - obj.height
                obj.vely = 0
                obj.accely = 0
                obj.grounded = True

            # COLLISION BETWEEN OBJS

            for o2 in self.objs:
                if o2 == obj:
                    continue

                if obj.grounded or o2.grounded:
                    # we check again because maybe we updated one of them inbetween
                    continue

                if obj.hitbox.colliderect(o2.hitbox):
                    obj.y = o2.y - obj.height
                    obj.vely = 0
                    obj.accely = 0
                    obj.grounded = True

    def add(self, obj: PhysicsObject):
        self.objs.append(obj)

    def remove(self, obj: PhysicsObject):
        self.objs.remove(obj)

    def apply_force(self, force: Sequence[int]):
        for obj in self.objs:
            if not obj.grounded:
                obj.accely += force[1]

            obj.accelx += force[0]

    def draw(self, surface: pygame.Surface):
        for obj in self.objs:
            obj.draw(surface)
