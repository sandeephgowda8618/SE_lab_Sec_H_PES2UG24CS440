"""
Coin: a static collectible circle. Drawn as a circle, hit-tested as a
bounding square around it.
"""

import pygame


class Coin:
    def __init__(self, x, y, radius=12, value=1, color=(230, 190, 60)):
        self.x = x
        self.y = y
        self.radius = radius
        self.value = value
        self.color = color

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.radius), int(self.y - self.radius),
            self.radius * 2, self.radius * 2,
        )
