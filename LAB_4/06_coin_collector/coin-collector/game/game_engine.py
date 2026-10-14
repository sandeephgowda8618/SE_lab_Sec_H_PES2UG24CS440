"""
GameEngine: owns the player, coins, and obstacles.

Obstacle collisions cost one life and return the player to the safe spawn.
"""

import math
import random
import time
import pygame

from game.player import Player
from game.coin import Coin
from game.collection import check_collection
from game.renderer import WIDTH, HEIGHT

NUM_COINS = 6
STARTING_LIVES = 3
ROUND_DURATION = 30
# BEGIN obstacle layout
OBSTACLE_LAYOUT = (
    (130, 110, 150, 24),
    (470, 95, 24, 130),
    (235, 340, 170, 24),
    (90, 285, 24, 125),
    (550, 360, 100, 24),
)
# END obstacle layout
# COIN_VALUE = 1  # Replaced by per-type values below.
# BEGIN coin type definitions
COIN_TYPES = {
    "bronze": (1, (205, 127, 50)),
    "silver": (3, (192, 192, 192)),
    "gold": (5, (255, 215, 0)),
}
# END coin type definitions


class GameEngine:
    def __init__(self):
        # BEGIN obstacle setup
        self.obstacles = [pygame.Rect(*bounds) for bounds in OBSTACLE_LAYOUT]
        # END obstacle setup
        self.reset_round()

    # BEGIN round timer and reset lifecycle
    def reset_round(self):
        self.player = Player(x=WIDTH / 2, y=HEIGHT / 2)
        self.coins = [self._random_coin() for _ in range(NUM_COINS)]
        self.score = 0
        self.lives = STARTING_LIVES
        self.time_remaining = ROUND_DURATION
        self.round_started_at = time.monotonic()
        self.game_over = False

    def _update_round_timer(self):
        if self.game_over:
            return
        self.time_remaining = max(
            0, ROUND_DURATION - (time.monotonic() - self.round_started_at)
        )
        if self.time_remaining <= 0:
            self.game_over = True
    # END round timer and reset lifecycle

    def _random_coin(self):
        while True:
            x = random.randint(30, WIDTH - 30)
            y = random.randint(30, HEIGHT - 30)
            coin_rect = pygame.Rect(x - 12, y - 12, 24, 24)
            if not any(coin_rect.colliderect(obstacle) for obstacle in self.obstacles):
                break
        # BEGIN randomized coin type assignment
        value, color = random.choice(tuple(COIN_TYPES.values()))
        return Coin(x=x, y=y, radius=12, value=value, color=color)
        # END randomized coin type assignment

    def handle_input(self, keys_pressed):
        self._update_round_timer()
        if self.game_over:
            if keys_pressed[pygame.K_r]:
                self.reset_round()
            return
        dx = dy = 0
        if keys_pressed[pygame.K_UP]:
            dy -= self.player.speed
        if keys_pressed[pygame.K_DOWN]:
            dy += self.player.speed
        if keys_pressed[pygame.K_LEFT]:
            dx -= self.player.speed
        if keys_pressed[pygame.K_RIGHT]:
            dx += self.player.speed
        self.player.move(dx, dy, WIDTH, HEIGHT)

    def update(self):
        self._update_round_timer()
        if self.game_over:
            return
        # BEGIN obstacle collision consequence
        if any(self.player.get_rect().colliderect(obstacle) for obstacle in self.obstacles):
            self.lives -= 1
            self.player.x = WIDTH / 2
            self.player.y = HEIGHT / 2
            if self.lives <= 0:
                self.game_over = True
            return
        # END obstacle collision consequence
        # BEGIN one-time coin collection
        collected = check_collection(self.player, self.coins)
        for coin in collected:
            self.score += coin.value
        self.coins = [coin for coin in self.coins if coin not in collected]
        # END one-time coin collection

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.player, self.coins, self.obstacles)
        # BEGIN round status display
        displayed_time = math.ceil(self.time_remaining)
        renderer.draw_text(
            surface,
            font,
            f"Score: {self.score}  Lives: {self.lives}  Time: {displayed_time}s",
            (10, 10),
        )
        # END round status display
        if self.game_over:
            # BEGIN round-over display and restart prompt
            renderer.draw_banner(surface, font, f"Final score: {self.score}")
            renderer.draw_text(
                surface, font, "Press R to start a new round", (10, HEIGHT - 32)
            )
            # END round-over display and restart prompt
