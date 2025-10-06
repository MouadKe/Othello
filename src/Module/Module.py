from View.constants import ROWS, COLS
from .util import square
from .util import status


class Module:
    def __init__(self):
        self.white = 2
        self.black = 2

        # Holds the empty squares that has a neighboor that isn't empty
        self.potentialPlays = self.createPotenial()

        # A representetive of the current board
        self.board = [[status.EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.board[3][3], self.board[4][4] = status.WHITE, status.WHITE
        self.board[3][4], self.board[4][3] = status.BLACK, status.BLACK

    def newPotential(self, block: square):
        # Define all 8 possible directions (row_offset, col_offset)
        directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]

        for row_offset, col_offset in directions:
            new_row = block.row + row_offset
            new_col = block.col + col_offset

            # Check if the new position is within bounds
            if (
                0 <= new_row < ROWS
                and 0 <= new_col < COLS
                and self.board[new_row][new_col] == status.EMPTY
            ):
                self.potentialPlays.add(square(new_row, new_col))

    def createPotenial(self):
        potentialPlays = set()

        # Add the 12 empty squares around the initial pieces
        for i in range(2, 6):
            potentialPlays.add(square(2, i))
            potentialPlays.add(square(5, i))

        for i in range(2, 6):
            potentialPlays.add(square(i, 2))
            potentialPlays.add(square(i, 5))

        return potentialPlays

    def availablePlays(self, Color, opColor):
        availablePlays = set()
        directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]

        for item in self.potentialPlays:
            row, col = item.row, item.col

            # Skip if the square is not empty (shouldn't happen, but safe)
            if self.board[row][col] != status.EMPTY:
                continue

            for dr, dc in directions:
                r, c = row + dr, col + dc
                found_opponent = False

                # Traverse in this direction
                while 0 <= r < ROWS and 0 <= c < COLS:
                    if self.board[r][c] == opColor:
                        found_opponent = True
                    elif self.board[r][c] == Color:
                        if found_opponent:
                            # Valid move: sandwiched opponent pieces
                            availablePlays.add(item)
                            break
                    else:  # status.EMPTY
                        break

                    r += dr
                    c += dc
                # End of direction loop — if valid, already added

        return availablePlays

    def updateBoard(self, block: square):

        change = []

        directions = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1),
        ]

        row, col = block.row, block.col

        if block.status == status.BLACK:
            Color = status.BLACK
            opColor = status.WHITE
        else:
            Color = status.WHITE
            opColor = status.BLACK

        for dr, dc in directions:
            r, c = row + dr, col + dc

            potentialChange = []
            isExtended = False
            # Traverse in this direction
            while 0 <= r < ROWS and 0 <= c < COLS:
                if self.board[r][c] == opColor and not isExtended:
                    potentialChange.append(square(r, c))
                elif self.board[r][c] == Color:
                    change.extend(potentialChange)
                    isExtended = True
                    break
                else:  # status.EMPTY
                    break

                r += dr
                c += dc

        for item in change:
            self.board[item.row][item.col] = Color
