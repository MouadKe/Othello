import pygame

from Model.Model import Model
from Model.util import status
from View.board import OthelloBoard
from View.constants import BLACK, WHITE
from Controller.controller import controller

model = Model()
Board = OthelloBoard()
control = controller(model, Board)

control.initGame()

running = True
while running:
    if control.turn == status.BLACK:
        Color = status.BLACK
        opColor = status.WHITE
        color = BLACK
    else:
        Color = status.WHITE
        opColor = status.BLACK
        color = WHITE

    availablePlays = model.availablePlays(Color, opColor, model.board)
    Board.draw_available(availablePlays, color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            control.handle_moves(mouse_x, mouse_y)
    pygame.display.update()
    Board.clock.tick(60)

pygame.quit()
# # pygame setup
# pygame.init()
# screen = pygame.display.set_mode((WIDTH, HEIGHT))
# clock = pygame.time.Clock()
# running = True
# dt = 0
# board = Board()
# board.draw_squares(screen)
#
# while running:
#     # poll for events
#     # pygame.QUIT event means the user clicked X to close your window
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#     # fill the screen with a color to wipe away anything from last frame
#     # flip() the display to put your work on screen
#     pygame.display.flip()
#
#     # limits FPS to 60
#     # dt is delta time in seconds since last frame, used for framerate-
#     # independent physics.
#     dt = clock.tick(60) / 1000
#
# pygame.quit()
