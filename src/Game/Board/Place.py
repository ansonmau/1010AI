from Game.Board.Board import Board


class PlaceUtils:
    def __init__(self, board: Board):
        self._board = board 

    def block(self, pos):
        assert self._board.check.check_block(pos)
        self._board.set(pos)

    def shape(self, shape, pos):
        assert self._board.check.check_shape(shape, pos)

        for curr_position in self._board.utils.get_shape_block_positions(shape, pos):
            self._board.set(curr_position)
