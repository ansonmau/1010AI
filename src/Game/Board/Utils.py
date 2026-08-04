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

    class ValidCheck:
        def get_all_valid_positions(self, shape: Shape):
            n_rows, n_cols = self._board.get_size()

            possiblePositions = []
            for row in range(self.board.numRows):
                for col in range(self.board.numCols):
                    currPos = (row, col)
                    if self.board.isValid.shape(shape, currPos):
                        possiblePositions.append(currPos)
                                    
            return possiblePositions
