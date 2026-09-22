from Game.Board.Clear import ClearUtils
from Game.Board.Place import PlaceUtils
from Game.Board.Utils import BoardUtils
from Game.Board.ValidCheck import ValidCheckUtils
from Game.Shape.Shape import Shape
import copy

class Board:
    DEFAULT_VALUE = False

    def __init__(self, nrows, ncols):
        self._nrows = nrows
        self._ncols = ncols
        self._rsize = nrows * ncols

        self._rboard      = self._generate_board()    # raw board
        self._prev_board  = self._generate_board()
        self._turn_count  = 0
        self._point_count = 0
        self._point_diff  = 0

        self.utils = BoardUtils(self)
        self.check = ValidCheckUtils(self)
        self.clear = ClearUtils(self)
        self.place = PlaceUtils(self)

    def play_shape(self, shape: Shape, pos):
        self._prev_board = copy.deepcopy(self._rboard)

        err = self.place.shape(shape, pos)
        if err:
            print("Failed to place shape. Wrong area?")
            return 1

        move = (shape, pos)
        pts_gained, cleared_rows, cleared_cols = self.clear.clear(move)

        for row in cleared_rows:
            self.clear.clear_row(row)
        for col in cleared_cols:
            self.clear.clear_col(col)

        # stat tracking
        self._point_diff   = pts_gained
        self._turn_count  += 1
        self._point_count += pts_gained

        return 0

    
    def get_turn_count(self):
        return self._turn_count

    def get_point_count(self):
        return self._point_count

    def get_point_diff(self):
        return self._point_diff

    def get_size(self):
        return (self._nrows, self._ncols)

    def get_board(self):
        return self._rboard

    def get_prev_board(self):
        return self._prev_board

    def dupe(self):
        new_board = Board(self._nrows, self._ncols)
        new_board._rboard = self._rboard.copy()

        return new_board

    def get(self, pos):
        row,col = pos

        return self._rboard[row][col]
    
    def get_row(self, row_num):
        return self._rboard[row_num]

    def get_col(self, col_num):
        return [row[col_num] for row in self._rboard]


    def set(self, pos):
        row,col = pos
        self._rboard[row][col] = True

    def unset(self, pos):
        row,col = pos
        self._rboard[row][col] = False

    def reset(self):
        self._rboard      = self._generate_board()
        self._point_count = 0
        self._point_diff  = 0
        self._turn_count  = 0

    def _generate_board(self):
        return [[Board.DEFAULT_VALUE for _ in range(self._ncols)] for _ in range(self._nrows)]

    @staticmethod
    def from_arr(arr):
        """
        create board from 2d array to use board functionality
        """
        nR = len(arr)
        nC = len(arr[0])

        b = Board(nR, nC)
        b._rboard = arr
        
        return b
