from Game.Shape.Shape import Shape

class BoardUtils:
    def __init__(self, board):
        self._board = board 

    def printBoard(self):
        n_rows, n_cols = self._board.get_size()

        for _ in range(n_cols + 2):     # +2 -> plus 1 for each "wall" on each side
            print("-", end = '   ')
        print()

        for row in self._board.get_board():
            print("|", end = '   ')
            for unit in row:
                print("X" if unit else ' ', end = '   ')
            print("|")

        for _ in range(n_cols + 2):
            print("-", end = '   ')
        print()

        return 

    
    def get_shape_block_positions(self, shape: Shape, pos: tuple):
        positions = []
        target_row, target_col = pos

        for dR, dC in shape.get_offsets():
            positions.append((target_row + dR, target_col + dC))
        
        return positions

    def get_filled_ratio(self):
        """
        returns ratio of how much of the board is used
        """
        n_rows, n_cols = self._board.get_size()

        total_positions = n_rows * n_cols
        filled_positions = 0

        for row in self._board.get_board():
            filled_positions += sum(1 for x in row if x != 0)
        
        return round(filled_positions / total_positions, 2)


    def calc_progress_score(self):
        blocks_pos = self._board.utils.get_shape_block_positions(shape, pos)
        rows = []
        cols = []

        # get unique rows and cols
        for row, col in blocks_pos:
            if row not in rows:
                rows.append(row)
            if col not in cols:
                cols.append(col)

        b = self._board.get_board()
        for row in rows:
            old_fill_count = sum(1 for x in b[row] if x != 0)
