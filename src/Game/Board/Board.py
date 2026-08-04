from Game.Board.Utils import BoardUtils
from Game.Board.ValidCheck import ValidCheck
from Game.Shape.Shape import Shape

class Board:
    DEFAULT_VALUE = False

    def __init__(self, nrows, ncols):
        self._nrows       = nrows
        self._ncols       = ncols

        self._r_board     = self._generate_board()    # raw board
        self._turn_count  = 0
        self._point_count = 0

        self.utils        = BoardUtils(self)
        self.check = ValidCheck(self)

    def place_shape(self, shape: Shape, position):
        pass 
    
    def get_turn_count(self):
        return self._turn_count

    def get_point_count(self):
        return self._point_count

    def get_size(self):
        return (self._nrows, self._ncols)

    def get_board(self):
        return self._r_board

    def reset(self):
        self._r_board     = self._generate_board()
        self._point_count = 0
        self._turn_count  = 0

    def _generate_board(self):
        return [[Board.DEFAULT_VALUE for _ in range(self._ncols)] for _ in range(self._nrows)]
