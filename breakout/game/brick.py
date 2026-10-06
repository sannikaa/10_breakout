"""
Brick: a single brick in the Breakout game.

Task 3 adds three brick types:
- Normal: breaks after 1 hit
- Strong: breaks after 2 hits
- Unbreakable: never breaks
"""

import pygame


class Brick:
    NORMAL = "normal"
    STRONG = "strong"
    UNBREAKABLE = "unbreakable"

    def __init__(
        self,
        x,
        y,
        width,
        height,
        brick_type=NORMAL
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.brick_type = brick_type

        if brick_type == self.NORMAL:
            self.hits_remaining = 1
            self.color = (200, 90, 90)

        elif brick_type == self.STRONG:
            self.hits_remaining = 2
            self.color = (230, 180, 60)

        elif brick_type == self.UNBREAKABLE:
            self.hits_remaining = -1
            self.color = (100, 100, 110)

        else:
            self.hits_remaining = 1
            self.color = (200, 90, 90)

    def get_rect(self):
        return pygame.Rect(
            int(self.x),
            int(self.y),
            self.width,
            self.height
        )

    def hit(self):
        """
        Apply a hit to the brick.

        Returns True if the brick should be removed.
        """
        if self.brick_type == self.UNBREAKABLE:
            return False

        self.hits_remaining -= 1

        # Strong brick changes appearance after first hit
        if (
            self.brick_type == self.STRONG
            and self.hits_remaining == 1
        ):
            self.color = (255, 220, 120)

        return self.hits_remaining <= 0