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
        pos = (gai_entry[1], gai_entry[2])
        return self.check_shape(shape, pos)

    def check_shape(self, shape: Shape, pos):
        def within_bounds(pos):
            return ( 0 <= pos[0] < self._nrows ) and ( 0 <= pos[1] < self._ncols )

        if ( shape.get_id() == 0 ):
            # null piece cannot be placed
            return False

        for block_position in self._board.utils.get_shape_block_positions(shape, pos):
            if ( not within_bounds(block_position) ) or ( self._board.get(block_position) ):
                    return False
                
        return True

    def get_all_valid_positions(self, shape: Shape):
        if shape.get_id() == 0: # null shape
            return []

        possiblePositions = []
        for row in range(self._nrows):
            for col in range(self._ncols):
                currPos = (row, col)
                if self.check_shape(shape, currPos):
                    possiblePositions.append(currPos)
                                
        return possiblePositions

