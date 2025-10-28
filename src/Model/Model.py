from View import board
from View.constants import ROWS, COLS
from .util import square, status, POSITION_WEIGHTS
import copy


class Model:
    def __init__(self):
        self.white = 2
        self.black = 2

        # Holds the empty squares that has a neighboor that isn't empty
        self.potentialPlays = self.createPotenial()

        # A representetive of the current board
        self.board = [[status.EMPTY for _ in range(COLS)] for _ in range(ROWS)]
        self.board[3][3], self.board[4][4] = status.WHITE, status.WHITE
        self.board[3][4], self.board[4][3] = status.BLACK, status.BLACK

    def newPotential(self, block: square, board):
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
                and board[new_row][new_col] == status.EMPTY
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

    def availablePlays(self, Color, opColor, board):
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
            if board[row][col] != status.EMPTY:
                continue

            for dr, dc in directions:
                r, c = row + dr, col + dc
                found_opponent = False

                # Traverse in this direction
                while 0 <= r < ROWS and 0 <= c < COLS:
                    if board[r][c] == opColor:
                        found_opponent = True
                    elif board[r][c] == Color:
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

    def updateBoard(self, block: square, board):

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
                if board[r][c] == opColor and not isExtended:
                    potentialChange.append(square(r, c))
                elif board[r][c] == Color:
                    change.extend(potentialChange)
                    isExtended = True
                    break
                else:  # status.EMPTY
                    break

                r += dr
                c += dc

        for item in change:
            board[item.row][item.col] = Color
        self.countPiecesBoard()

    def countPiecesBoard(self):
        white = 0
        black = 0
        for i in range(ROWS):
            for j in range(COLS):
                if self.board[i][j] == status.BLACK:
                    black += 1
                elif self.board[i][j] == status.WHITE:
                    white += 1

        self.white = white
        self.black = black

    def countPieces(self, board):
        white = 0
        black = 0
        for i in range(ROWS):
            for j in range(COLS):
                if board[i][j] == status.BLACK:
                    black += 1
                elif board[i][j] == status.WHITE:
                    white += 1

        return [black, white]

    def createState(self, board, block):
        newBoard = copy.deepcopy(board)
        newBoard[block.row][block.col] = block.status
        self.updateBoard(block, newBoard)

        return newBoard

    def evaluate_board(self, board, player):
        if player == status.WHITE:
            opponent = status.BLACK
        else:
            opponent = status.WHITE

        positional_score = 0
        for i in range(8):
            for j in range(8):
                if board[i][j] == player:
                    positional_score += POSITION_WEIGHTS[i][j]
                elif board[i][j] == opponent:
                    positional_score -= POSITION_WEIGHTS[i][j]
        return positional_score

    def isTerminal(self, board):
        pieces = self.countPieces(board)
        total = pieces[0] + pieces[1]
        if total == 64:
            return True
        return False

    def minimax(self, board, depth, alpha, beta, maximizingPlayer, player):
        if player == status.WHITE:
            opponent = status.BLACK
        else:
            opponent = status.WHITE

        if depth == 0 or self.isTerminal(board):
            return self.evaluate_board(board, player)

        # ---  Maximizing player ---
        if maximizingPlayer:
            maxEval = float("-inf")

            available_moves = self.availablePlays(player, opponent, board)

            # If no moves available → pass turn or evaluate board
            if not available_moves:
                return self.evaluate_board(board, player)

            for move in available_moves:

                new_board = self.createState(board, square(move.row, move.col, player))

                eval = self.minimax(new_board, depth - 1, alpha, beta, False, player)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)

                if beta <= alpha:
                    break

            return maxEval

        # ---  Minimizing player ---
        else:
            minEval = float("inf")

            available_moves = self.availablePlays(opponent, player, board)

            if not available_moves:
                return self.evaluate_board(board, player)

            for move in available_moves:
                new_board = self.createState(
                    board, square(move.row, move.col, opponent)
                )

                eval = self.minimax(new_board, depth - 1, alpha, beta, True, player)
                minEval = min(minEval, eval)
                beta = min(beta, eval)

                if beta <= alpha:
                    break

            return minEval

    def botPlay(self):
        best_move = None
        best_value = float("-inf")

        player = status.WHITE
        opponent = status.BLACK
        depth = 4  

        for move in self.availablePlays(player, opponent, self.board):
            new_board = self.createState(self.board, square(move.row, move.col, player))
            eval = self.minimax(
                new_board, depth - 1, float("-inf"), float("inf"), False, player
            )
            if eval > best_value:
                best_value = eval
                best_move = move
        if best_move:
            self.board[best_move.row][best_move.col] = status.WHITE
            self.updateBoard(best_move, self.board)
            self.newPotential(best_move, self.board)
