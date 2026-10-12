"""
Helicopter: the player-controlled vehicle. Moves vertically based on
held Up/Down keys.
"""

import pygame

THRUST = 0.4
MAX_SPEED = 5.0


class Helicopter:
    def __init__(self, x, y, width=40, height=24):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vy = 0.0
        self.shield_active = False

    def handle_input(self, keys_pressed):
        if keys_pressed[pygame.K_UP]:
            self.vy -= THRUST
        if keys_pressed[pygame.K_DOWN]:
            self.vy += THRUST
        self.vy = max(-MAX_SPEED, min(self.vy, MAX_SPEED))

    def update(self, height_bound):
        self.y += self.vy
        half_height = self.height / 2
        if self.y - half_height < 0:
            self.y = half_height
            self.vy = 0
        elif self.y + half_height > height_bound:
            self.y = height_bound - half_height
            self.vy = 0

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2), int(self.y - self.height / 2),
            self.width, self.height,
        )
