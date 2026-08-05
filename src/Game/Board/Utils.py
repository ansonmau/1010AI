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

