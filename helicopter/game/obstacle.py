"""
Obstacle: a scrolling wall pair with a gap the helicopter must fly
through.
"""

import pygame


class Obstacle:
    def __init__(self, x, gap_y, gap_height, wall_width, screen_height, speed):
        self.x = x
        self.gap_y = gap_y
        self.gap_height = gap_height
        self.wall_width = wall_width
        self.screen_height = screen_height
        self.speed = speed
        self.scored = False   # used for distance/pass tracking later
        self.collided = False

    def update(self):
        self.x -= self.speed

    def is_off_screen(self):
        return self.x + self.wall_width < 0

    def get_top_rect(self):
        top_height = self.gap_y - self.gap_height / 2
        return pygame.Rect(int(self.x), 0, self.wall_width, int(top_height))

    def get_bottom_rect(self):
        bottom_y = self.gap_y + self.gap_height / 2
        return pygame.Rect(int(self.x), int(bottom_y), self.wall_width, int(self.screen_height - bottom_y))
