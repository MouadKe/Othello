import pygame
from Model.Model import Model
from Model.util import status
from View.board import OthelloBoard
from View.constants import HEIGHT_OFFSET, SQUARE_SIZE, WIDTH_OFFSET
import time

class controller:
    def __init__(self, model: Model, view: OthelloBoard):
        self.turn = status.BLACK
        self.model = model
        self.view = view

    def initGame(self):
        self.view.updateBoard(self.view.win, self.model.board)

    def changeStatus(self):
        if self.turn == status.BLACK:
            self.turn = status.WHITE
        else:
            self.turn = status.BLACK

    def handle_moves(self, mouse_x, mouse_y):
        if self.turn == status.BLACK:
            Color = status.BLACK
            opColor = status.WHITE
        else:
            Color = status.WHITE
            opColor = status.BLACK

        availablePlays = self.model.availablePlays(Color, opColor, self.model.board)
        for item in availablePlays:
            minx = WIDTH_OFFSET + item.col * SQUARE_SIZE
            maxx = WIDTH_OFFSET + item.col * SQUARE_SIZE + SQUARE_SIZE
            miny = HEIGHT_OFFSET + item.row * SQUARE_SIZE
            maxy = HEIGHT_OFFSET + item.row * SQUARE_SIZE + SQUARE_SIZE
            if minx < mouse_x and mouse_x < maxx and miny < mouse_y and mouse_y < maxy:
                self.model.board[item.row][item.col] = Color
                #self.changeStatus()
                item.status = Color
                self.model.updateBoard(item, self.model.board)
                self.model.newPotential(item, self.model.board)
                self.view.updateBoard(self.view.win, self.model.board)
                self.model.botPlay()
                self.view.updateBoard(self.view.win, self.model.board)
