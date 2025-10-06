import pygame

from Module.Module import Module
from Module.util import status
from View.board import OthelloBoard

module = Module()
print(module.board)
for item in module.potentialPlays:
    print(item.row, item.col, item.status)
availablePlays = module.availablePlays(status.BLACK, status.WHITE)
print(availablePlays)

item = availablePlays.pop()
item.status = status.BLACK
module.updateBoard(item)

print(module.board)

Board = OthelloBoard()
Board.run()

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
