import pygame
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
from Model.util import status


class OthelloBoard:
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Othello Board")
        self.background = self.load_image("assets/background.png", (WIDTH, HEIGHT))
        self.sidelines = self.load_image("assets/boardside.png", (1000, 1000))
        self.board_texture = self.load_image(
            "assets/wood.jpg", (BOARD_WIDTH, BOARD_HEIGHT)
        )
        self.clock = pygame.time.Clock()

    def load_image(self, filename, size):

        try:
            img = pygame.image.load(filename).convert()
            return pygame.transform.scale(img, size)
        except pygame.error:
            print(filename + "not found")

    def draw_squares(self, win):

        win.blit(self.background, (0, 0))
        # Draw textured background
        # win.blit(self.sidelines, (WIDTH_OFFSET, HEIGHT_OFFSET))

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
        pygame.draw.circle(
            win,
            WHITE,
            (center_x - highlight_offset, center_y - highlight_offset),
            highlight_radius,
        )

    def draw_available(self, availblePlays, color):
        circle_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.Surface.convert_alpha(circle_surface)

        for item in availblePlays:
            self.draw_piece(circle_surface, item.row, item.col, (255, 0, 0))

        opacity = 64
        circle_surface.set_alpha(opacity)
        self.win.blit(circle_surface, (0, 0))

    def updateBoard(self, win, board):
        self.draw_squares(win)

        for i in range(ROWS):
            for j in range(COLS):
                item = board[i][j]
                if item == status.BLACK:
                    self.draw_piece(win, i, j, BLACK)
                elif item == status.WHITE:
                    self.draw_piece(win, i, j, WHITE)
