from Game.Board.Clear import ClearUtils
from Game.Board.Place import PlaceUtils
from Game.Board.Utils import BoardUtils
from Game.Board.ValidCheck import ValidCheckUtils
from Game.Shape.Shape import Shape

class Board:
    DEFAULT_VALUE = False

    def __init__(self, nrows, ncols):
        self._nrows = nrows
        self._ncols = ncols
        self._rsize = nrows * ncols

        self._rboard      = self._generate_board()    # raw board
        self._turn_count  = 0
        self._point_count = 0
        self._point_diff  = 0
        self._filled      = 0

        self.utils = BoardUtils(self)
        self.check = ValidCheckUtils(self)
        self.clear = ClearUtils(self)
        self.place = PlaceUtils(self)

    def play_shape(self, shape: Shape, pos):
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
        self._filled      += shape.get_volume()

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

    def get_filled_ratio(self):
        return round(self._filled / self._rsize, 2)

    def get(self, pos):
        row,col = pos

        assert row < self._nrows
        assert col < self._ncols

        return self._rboard[row][col]

    def set(self, pos):
        row,col = pos
        self._rboard[row][col] = True

    def unset(self, pos):
        row,col = pos
        self._rboard[row][col] = False

    def reset(self):
        self._rboard      = self._generate_board()
        self._point_count = 0
        self._filled      = 0
        self._point_diff  = 0
        self._turn_count  = 0

    def _generate_board(self):
        return [[Board.DEFAULT_VALUE for _ in range(self._ncols)] for _ in range(self._nrows)]
