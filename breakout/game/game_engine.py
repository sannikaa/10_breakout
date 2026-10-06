"""
GameEngine: owns the paddle, ball, and bricks.

Tasks:
1. Brick collision and removal
2. Lives and Game Over
3. Normal, Strong, and Unbreakable bricks
4. Score and combo multiplier
"""

import pygame

from game.paddle import Paddle
from game.ball import Ball
from game.brick import Brick
from game.collision import handle_ball_brick_collision
from game.renderer import WIDTH, HEIGHT

BRICK_ROWS = 4
BRICK_COLS = 8
BRICK_WIDTH = 68
BRICK_HEIGHT = 22
BRICK_GAP = 6
BRICK_TOP_MARGIN = 50

STARTING_LIVES = 3


class GameEngine:
    def __init__(self):
        self.paddle = Paddle(x=WIDTH / 2, y=HEIGHT - 30)
        self.ball = Ball(x=WIDTH / 2, y=HEIGHT - 50)

        self.bricks = self._build_bricks()

        self.lives = STARTING_LIVES
        self.game_over = False

        # Task 4: score and combo
        self.score = 0
        self.combo = 1

    def _build_bricks(self):
        bricks = []

        total_width = (
            BRICK_COLS * (BRICK_WIDTH + BRICK_GAP)
            - BRICK_GAP
        )

        start_x = (WIDTH - total_width) / 2

        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = start_x + col * (BRICK_WIDTH + BRICK_GAP)
                y = BRICK_TOP_MARGIN + row * (
                    BRICK_HEIGHT + BRICK_GAP
                )

                if row == 0:
                    brick_type = Brick.UNBREAKABLE
                elif row == 1:
                    brick_type = Brick.STRONG
                else:
                    brick_type = Brick.NORMAL

                bricks.append(
                    Brick(
                        x,
                        y,
                        BRICK_WIDTH,
                        BRICK_HEIGHT,
                        brick_type
                    )
                )

        return bricks

    def _reset_ball(self):
        self.ball = Ball(
            x=WIDTH / 2,
            y=HEIGHT - 50
        )

    def restart(self):
        self.paddle = Paddle(
            x=WIDTH / 2,
            y=HEIGHT - 30
        )

        self.ball = Ball(
            x=WIDTH / 2,
            y=HEIGHT - 50
        )

        self.bricks = self._build_bricks()

        self.lives = STARTING_LIVES
        self.game_over = False

        self.score = 0
        self.combo = 1

    def handle_input(self, keys_pressed):
        if self.game_over:
            return

        dx = 0

        if keys_pressed[pygame.K_LEFT]:
            dx -= self.paddle.speed

        if keys_pressed[pygame.K_RIGHT]:
            dx += self.paddle.speed

        self.paddle.move(dx, WIDTH)

    def handle_keydown(self, key):
        if self.game_over and key == pygame.K_r:
            self.restart()

    def update(self):
        if self.game_over:
            return

        self.ball.update()
        self.ball.bounce_off_walls(WIDTH)

        # Ball hitting paddle
        if (
            self.ball.get_rect().colliderect(
                self.paddle.get_rect()
            )
            and self.ball.vy > 0
        ):
            self.ball.bounce_off_paddle(
                self.paddle.get_rect()
            )

        # Ball hitting bricks
        for brick in self.bricks:

            if handle_ball_brick_collision(
                self.ball,
                brick
            ):

                # Unbreakable bricks do not give points
                # and do not disappear.
                if brick.brick_type == Brick.UNBREAKABLE:
                    break

                # Apply hit to brick
                brick_removed = brick.hit()

                # Task 4: award points for every successful
                # hit on a breakable brick.
                self.score += 10 * self.combo

                # Increase combo after a successful hit.
                self.combo += 1

                # Remove brick when completely broken.
                if brick_removed:
                    self.bricks.remove(brick)

                break

        # Ball falls below the screen
        if self.ball.is_below(HEIGHT):
            self.lives -= 1

            # Task 4: missing the ball resets combo.
            self.combo = 1

            if self.lives <= 0:
                self.game_over = True
            else:
                self._reset_ball()

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(
            surface,
            self.paddle,
            self.ball,
            self.bricks
        )

        renderer.draw_text(
            surface,
            font,
            f"Bricks left: {len(self.bricks)}",
            (10, 10)
        )

        renderer.draw_text(
            surface,
            font,
            f"Lives: {self.lives}",
            (10, 35)
        )

        # Task 4: display score
        renderer.draw_text(
            surface,
            font,
            f"Score: {self.score}",
            (10, 60)
        )

        # Task 4: display combo
        renderer.draw_text(
            surface,
            font,
            f"Combo: x{self.combo}",
            (10, 85)
        )

        if self.game_over:
            renderer.draw_text(
                surface,
                font,
                "GAME OVER - Press R to Restart",
                (WIDTH / 2 - 150, HEIGHT / 2)
            )