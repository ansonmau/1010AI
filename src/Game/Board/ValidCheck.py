from Game.Shape.Shape import Shape

class ValidCheckUtils:
    def __init__(self, board):
        self._board = board 
        self._nrows, self._ncols = self._board.get_size()

    # ╭────────────────────────────────────────────────╮
    # │                    Helpers                     │
    # ╰────────────────────────────────────────────────╯
    def _is_empty(self, pos):
        row, col = pos
        return self._board.get_board()[row][col] == False


    # ╭────────────────────────────────────────────────╮
    # │                      API                       │
    # ╰────────────────────────────────────────────────╯
    def check_block(self, pos):
        row, col = pos 
        if (0 <= row < self._nrows) and (0 <= col < self._ncols):
            if self._is_empty(pos):
                return True 
        return False

    def check_gai(self, gai_entry):
        # (shape_id, row, col)
        shape = Shape(gai_entry[0])
        return self.check_shape(shape, (gai_entry[1], gai_entry[2]))

    def check_shape(self, shape: Shape, pos):
        if shape.get_id() == 0:
            # null piece cannot be placed
            return False

        row,col = pos
        shape_height, shape_width = shape.get_dimensions()

        # check if shape would even fit on the board at pos
        # if 2x2, then it should check row+1 and col+1 assuming top left corner start
        if (row + shape_height - 1) > self._nrows - 1 or (col + shape_width - 1) > self._ncols - 1:
            return False

        # check if any positions are already filled
        for block_position in self._board.utils.get_shape_block_positions(shape, pos):
            if not self._is_empty(block_position):
                    return False
                
        return True

    def get_all_valid_positions(self, shape: Shape):
        possiblePositions = []
        for row in range(self._nrows):
            for col in range(self._ncols):
                currPos = (row, col)
                if self.check_shape(shape, currPos):
                    possiblePositions.append(currPos)
                                
        return possiblePositions
