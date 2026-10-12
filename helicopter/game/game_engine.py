"""
GameEngine: owns the helicopter and all obstacles.

Starter version: the helicopter moves and obstacles scroll by, but
there's no collision detection at all yet (the helicopter can fly
straight through obstacles harmlessly), no scoring, and no shield.
That's Tasks 2, 3, and 4. Movement also has known bugs (see
game/helicopter.py) that Task 1 asks you to fix.
"""

import pygame
import random

from game.helicopter import Helicopter
from game.obstacle import Obstacle
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 90
GAP_HEIGHT = 150
WALL_WIDTH = 60
SCROLL_SPEED = 3


class GameEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        self.helicopter = Helicopter(x=100, y=HEIGHT / 2)
        self.obstacles = []
        self.frames_until_spawn = 0
        self.distance = 0
        self.game_over = False

    def _spawn_obstacle(self):
        margin = 60
        gap_y = random.randint(margin + GAP_HEIGHT // 2, HEIGHT - margin - GAP_HEIGHT // 2)
        self.obstacles.append(Obstacle(
            x=WIDTH, gap_y=gap_y, gap_height=GAP_HEIGHT,
            wall_width=WALL_WIDTH, screen_height=HEIGHT, speed=SCROLL_SPEED,
        ))

    def handle_input(self, keys_pressed):
        if not self.game_over:
            self.helicopter.handle_input(keys_pressed)

    def handle_keydown(self, key):
        if self.game_over:
            if key in (pygame.K_SPACE, pygame.K_r, pygame.K_RETURN):
                self.reset()
        else:
            if key in (pygame.K_SPACE, pygame.K_s):
                self.helicopter.shield_active = True

    def update(self):
        if self.game_over:
            return

        self.distance += 1
        self.helicopter.update(HEIGHT)

        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            self._spawn_obstacle()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        for obstacle in self.obstacles:
            obstacle.update()
        self.obstacles = [o for o in self.obstacles if not o.is_off_screen()]

        # Collision detection between helicopter and obstacles
        heli_rect = self.helicopter.get_rect()
        for obstacle in self.obstacles:
            if not obstacle.collided:
                if heli_rect.colliderect(obstacle.get_top_rect()) or heli_rect.colliderect(obstacle.get_bottom_rect()):
                    if self.helicopter.shield_active:
                        self.helicopter.shield_active = False
                        obstacle.collided = True
                    else:
                        self.game_over = True
                        break

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.helicopter, self.obstacles)

        # Distance score
        renderer.draw_text(surface, font, f"Distance: {self.distance}m", (20, 20))

        # Shield status indicator
        if self.helicopter.shield_active:
            renderer.draw_text(surface, font, "Shield: ACTIVE", (20, 50), color=(0, 140, 220))
        else:
            renderer.draw_text(surface, font, "Shield: READY (SPACE)", (20, 50), color=(80, 80, 80))

        # Game over banner and final distance
        if self.game_over:
            renderer.draw_banner(surface, font, "GAME OVER - Press R to Restart")
            final_surf = font.render(f"Final Distance: {self.distance}m", True, (20, 20, 20))
            final_rect = final_surf.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2 + 35))
            surface.blit(final_surf, final_rect)
