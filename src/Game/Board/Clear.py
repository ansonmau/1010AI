from typing import TYPE_CHECKING
from Game.Shape.Shape import Shape

if TYPE_CHECKING:
    from Game.Board.Board import Board

class ClearUtils:
        def __init__(self, board: "Board"):
                self._board = board
                self._nrows, self._ncols = self._board.get_size()

        def clear(self, move_tuple):
                total_cleared = 0
                colsCleared   = []
                rowsCleared   = []
                shape, pos    = move_tuple

                blocks_pos = self._board.utils.get_shape_block_positions(shape, pos)
                for row, col in blocks_pos:
                        if (col not in colsCleared) and self._check_col(col):
                                colsCleared.append(col)
                        if (row not in rowsCleared) and self._check_row(row):
                                rowsCleared.append(row)

                total_cleared = len(colsCleared) + len(rowsCleared)
                
                if total_cleared > 0:
                        # points = (100 + 200*(total_cleared-1))
                        points = 100 * total_cleared
                else:
                        points = 0
                        
                return points, rowsCleared, colsCleared
        
        def simulate(self, shape, pos):
                colsCleared = []
                rowsCleared = []
                
                blocks_pos = self._board.utils.get_shape_block_positions(shape, pos)
                for row, col in blocks_pos:
                        if col not in colsCleared and self._check_col_with_mask(col, blocks_pos):
                                colsCleared.append(col)
                        if row not in rowsCleared and self._check_row_with_mask(row, blocks_pos):
                                rowsCleared.append(row)
                
                total_cleared = len(colsCleared) + len(rowsCleared)
                if total_cleared > 0:
                        points = 100 + 200*(total_cleared-1)
                else:
                        points = 0

                return points, rowsCleared, colsCleared



        
        def clear_col(self, col):
                for i in range(self._nrows):
                    pos = (i,col)
                    self._board.unset(pos)
                return
        
        def clear_row(self, row):
                for i in range(self._ncols):
                    pos = (row,i)
                    self._board.unset(pos)
                return

        def _check_col(self, col):
                for i in range(self._nrows):
                        pos = (i,col)
                        if not self._board.get(pos):
                                return False
                return True

        def _check_row(self, row):
                for i in range(self._ncols):
                        pos = (row,i)
                        if not self._board.get(pos):
                                return False
                return True

        def _check_col_with_mask(self, col, shapeCoords):
                for i in range(self._nrows):
                        currPos = (i, col)
                        if not self._board.get(currPos) and currPos not in shapeCoords:
                                return False
                return True

        def _check_row_with_mask(self, row, shapeCoords):
                for i in range(self._ncols):
                        currPos = (row, i)
                        if not self._board.get(currPos) and currPos not in shapeCoords:
                                return False
                return True


