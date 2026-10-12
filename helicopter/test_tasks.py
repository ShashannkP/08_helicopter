import pygame
from game.helicopter import Helicopter
from game.obstacle import Obstacle
from game.game_engine import GameEngine

def run_tests():
    print("--- Running Tests ---")

    # ==========================
    # Task 1: Movement & Boundaries
    # ==========================
    h = Helicopter(100, 250)
    keys_down = {pygame.K_UP: False, pygame.K_DOWN: True}
    for _ in range(120):
        h.handle_input(keys_down)
    assert abs(h.vy) <= 5.0, f"Speed cap failed: {h.vy}"

    h.update(500)
    assert h.get_rect().bottom <= 500, "Bottom boundary clamp failed"

    # ==========================
    # Task 2: Obstacle Collision & Game Over
    # ==========================
    engine = GameEngine()
    assert not engine.game_over, "Game should not start in game_over state"

    # Create obstacle with gap at y=250, height=150 (gap from 175 to 325)
    # Helicopter at x=100, y=250 is safely in gap
    obs_gap = Obstacle(x=100, gap_y=250, gap_height=150, wall_width=60, screen_height=500, speed=0)
    engine.obstacles = [obs_gap]
    engine.update()
    assert not engine.game_over, "Helicopter safely in gap should NOT trigger game over"

    # Move helicopter into top wall: y=100 (top wall goes from 0 to 175)
    engine.helicopter.y = 100
    engine.update()
    assert engine.game_over, "Touching top wall of obstacle MUST trigger game over"

    # Reset and test bottom wall collision
    engine.reset()
    assert not engine.game_over, "Reset must clear game_over"
    engine.obstacles = [obs_gap]
    engine.helicopter.y = 400  # bottom wall starts at 325
    engine.update()
    assert engine.game_over, "Touching bottom wall of obstacle MUST trigger game over"

    # ==========================
    # Task 2 Detailed Edge Cases: Gap margins & Wall touches
    # ==========================
    engine.reset()
    # Obstacle with gap from y=175 to y=325 (height 150, center 250)
    # Helicopter height is 24, so half_height is 12.
    obs = Obstacle(x=100, gap_y=250, gap_height=150, wall_width=60, screen_height=500, speed=0)
    engine.obstacles = [obs]

    # Heli center at 187 -> top is 175, exactly flush with bottom of top wall, no intersection
    engine.helicopter.y = 187
    engine.update()
    assert not engine.game_over, "Flush with top wall without overlapping must NOT collide"

    # Heli center at 313 -> bottom is 325, exactly flush with top of bottom wall, no intersection
    engine.helicopter.y = 313
    engine.update()
    assert not engine.game_over, "Flush with bottom wall without overlapping must NOT collide"

    # Heli center at 186 -> top is 174, 1px overlap with top wall
    engine.helicopter.y = 186
    engine.update()
    assert engine.game_over, "1px overlap with top wall MUST trigger game over"

    # ==========================
    # Task 3: Distance-based scoring
    # ==========================
    engine.reset()
    assert engine.distance == 0, "Distance must start at 0"
    engine.obstacles = []  # no obstacles so it won't crash
    engine.update()
    assert engine.distance == 1, f"Distance should increase by 1 per frame, got {engine.distance}"
    for _ in range(59):
        engine.update()
    assert engine.distance == 60, f"Distance should climb steadily, got {engine.distance}"

    # Verify distance freezes on game over
    engine.game_over = True
    dist_at_death = engine.distance
    engine.update()
    assert engine.distance == dist_at_death, "Distance must freeze when game is over"

    # Verify reset with 'r' key
    engine.handle_keydown(pygame.K_r)
    assert not engine.game_over, "Pressing R must restart the game"
    assert engine.distance == 0, "Reset must reset distance back to 0"

    # Verify reset with SPACE key
    engine.game_over = True
    engine.handle_keydown(pygame.K_SPACE)
    assert not engine.game_over, "Pressing SPACE on game over must restart the game"
    assert engine.distance == 0, "Reset must reset distance back to 0"

    # ==========================
    # Task 4: Shield mechanic & Reactivation
    # ==========================
    engine.reset()
    assert not engine.helicopter.shield_active, "Shield should initially be inactive"
    engine.handle_keydown(pygame.K_SPACE)
    assert engine.helicopter.shield_active, "Pressing SPACE should activate shield"

    # Test shield absorbs collision
    obs_hit = Obstacle(x=100, gap_y=450, gap_height=50, wall_width=60, screen_height=500, speed=0)
    engine.obstacles = [obs_hit]
    engine.helicopter.y = 250
    engine.update()
    assert not engine.game_over, "Shield must protect helicopter from collision"
    assert not engine.helicopter.shield_active, "Shield must disappear/turn off after absorbing collision"

    # Helicopter now vulnerable: another obstacle collision should cause game over
    obs_hit2 = Obstacle(x=100, gap_y=450, gap_height=50, wall_width=60, screen_height=500, speed=0)
    engine.obstacles = [obs_hit2]
    engine.update()
    assert engine.game_over, "Helicopter should be vulnerable after shield is used"

    # Test reactivating shield after absorbing a hit (while still alive in a run)
    engine.reset()
    engine.handle_keydown(pygame.K_SPACE)
    assert engine.helicopter.shield_active, "Shield activated"
    obs1 = Obstacle(x=100, gap_y=450, gap_height=50, wall_width=60, screen_height=500, speed=0)
    engine.obstacles = [obs1]
    engine.helicopter.y = 250
    engine.update()
    assert not engine.game_over, "Shield absorbed hit 1"
    assert not engine.helicopter.shield_active, "Shield consumed"

    # Reactivate shield for next obstacle
    engine.handle_keydown(pygame.K_SPACE)
    assert engine.helicopter.shield_active, "Shield reactivated for next encounter"
    obs2 = Obstacle(x=100, gap_y=450, gap_height=50, wall_width=60, screen_height=500, speed=0)
    engine.obstacles = [obs2]
    engine.update()
    assert not engine.game_over, "Reactivated shield absorbed hit 2"
    assert not engine.helicopter.shield_active, "Shield consumed again"

    print("ALL TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()
