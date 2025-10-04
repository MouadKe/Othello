from enum import Enum


class status(Enum):
    EMPTY = 0
    WHITE = 1
    BLACK = 2


class square:
    def __init__(self, row, col, status=status.EMPTY):
        self.row = row
        self.col = col
        self.status = status

    def __eq__(self, other):

        if isinstance(other, square):
            return (
                self.row == other.row
                and self.col == other.col
                and self.status == other.status
            )
        return False

    def __hash__(self):

        return hash((self.row, self.col, self.status))

    def __repr__(self):

        return f"square({self.row}, {self.col}, {self.status})"
