"""
GameEngine: owns the paddle, ball, and bricks.

Task 1:
- Fix brick collision so bricks are removed correctly.

Task 2:
- Add 3 lives.
- Lose a life when the ball falls below the paddle.
- Reset the ball after losing a life.
- Show Game Over when all lives are lost.
- Allow the player to restart.
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

        # Task 2: player starts with 3 lives
        self.lives = STARTING_LIVES

        # Task 2: game-over state
        self.game_over = False

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

                bricks.append(
                    Brick(
                        x,
                        y,
                        BRICK_WIDTH,
                        BRICK_HEIGHT
                    )
                )

        return bricks

    def _reset_ball(self):
        self.ball = Ball(
            x=WIDTH / 2,
            y=HEIGHT - 50
        )

    def restart(self):
        """
        Restart the game after Game Over.
        """
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

    def handle_input(self, keys_pressed):
        # Don't move the paddle after Game Over
        if self.game_over:
            return

        dx = 0

        if keys_pressed[pygame.K_LEFT]:
            dx -= self.paddle.speed

        if keys_pressed[pygame.K_RIGHT]:
            dx += self.paddle.speed

        self.paddle.move(dx, WIDTH)

    def handle_keydown(self, key):
        # Restart the game by pressing R
        if self.game_over and key == pygame.K_r:
            self.restart()

    def update(self):
        # Don't update the game after Game Over
        if self.game_over:
            return

        self.ball.update()

        self.ball.bounce_off_walls(WIDTH)

        # Ball hitting the paddle
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
                brick.hits_remaining -= 1

                # Task 1:
                # Remove brick when its hits are finished.
                if brick.hits_remaining <= 0:
                    self.bricks.remove(brick)

                break

        # Ball falls below the screen
        if self.ball.is_below(HEIGHT):
            self.lives -= 1

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

        # Show number of bricks remaining
        renderer.draw_text(
            surface,
            font,
            f"Bricks left: {len(self.bricks)}",
            (10, 10)
        )

        # Task 2: show lives
        renderer.draw_text(
            surface,
            font,
            f"Lives: {self.lives}",
            (10, 35)
        )

        # Task 2: show Game Over
        if self.game_over:
            renderer.draw_text(
                surface,
                font,
                "GAME OVER - Press R to Restart",
                (WIDTH / 2 - 150, HEIGHT / 2)
            )