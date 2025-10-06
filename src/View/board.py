import pygame
import sys
from .constants import (
    BOARD_WIDTH,
    HEIGHT_OFFSET,
    WIDTH,
    HEIGHT,
    ROWS,
    COLS,
    SQUARE_SIZE,
    GRID_COLOR,
    PADDING,
    WHITE,
    BLACK,
    BOARD_COLOR,
    WIDTH_OFFSET,
    BOARD_HEIGHT,
)


class OthelloBoard:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Othello Board with Textures")
        self.board_texture = self.load_texture(
            "assets/wood.jpg", (BOARD_WIDTH, BOARD_HEIGHT)
        )
        self.clock = pygame.time.Clock()

    def load_texture(self, filename, size):

        try:
            img = pygame.image.load(filename).convert()
            return pygame.transform.scale(img, size)
        except pygame.error:
            print("wood.jpg not foung")

    def draw_squares(self, win):
        # Draw textured background
        win.blit(self.board_texture, (WIDTH_OFFSET, HEIGHT_OFFSET))

        # Draw grid lines to separate squares
        for row in range(ROWS + 1):
            y = row * SQUARE_SIZE + HEIGHT_OFFSET
            pygame.draw.line(
                win, GRID_COLOR, (WIDTH_OFFSET, y), (BOARD_WIDTH + WIDTH_OFFSET, y), 3
            )
        for col in range(COLS + 1):
            x = col * SQUARE_SIZE + WIDTH_OFFSET
            pygame.draw.line(
                win,
                GRID_COLOR,
                (x, HEIGHT_OFFSET),
                (x, BOARD_HEIGHT + HEIGHT_OFFSET),
                3,
            )

        # Optional: Draw slightly inset squares for depth (uncomment if needed)
        # for row in range(ROWS):
        #     for col in range(COLS):
        #         rect = pygame.Rect(
        #             col * SQUARE_SIZE + PADDING,
        #             row * SQUARE_SIZE + PADDING,
        #             SQUARE_SIZE - 2 * PADDING,
        #             SQUARE_SIZE - 2 * PADDING
        #         )
        #         pygame.draw.rect(win, BOARD_COLOR, rect, border_radius=3)

    def draw_piece(self, win, row, col, color):
        """Draw a piece with a subtle 3D effect."""
        center_x = (col * SQUARE_SIZE + SQUARE_SIZE // 2) + WIDTH_OFFSET
        center_y = (row * SQUARE_SIZE + SQUARE_SIZE // 2) + HEIGHT_OFFSET
        radius = SQUARE_SIZE // 2 - PADDING * 2

        # Main circle
        pygame.draw.circle(win, color, (center_x, center_y), radius)

        # Highlight for 3D effect
        highlight_radius = radius // 3
        highlight_offset = radius // 4
        highlight_color = (255, 255, 255, 150)
        pygame.draw.circle(
            win,
            WHITE,
            (center_x - highlight_offset, center_y - highlight_offset),
            highlight_radius,
        )

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.draw_squares(self.win)

            # Draw initial Othello pieces (example)
            self.draw_piece(self.win, 3, 3, WHITE)
            self.draw_piece(self.win, 3, 4, BLACK)
            self.draw_piece(self.win, 4, 3, BLACK)
            self.draw_piece(self.win, 4, 4, WHITE)

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = OthelloBoard()
    game.run()
