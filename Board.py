from Shape import Shape

class Board:
        def __init__(self, numRows, numCols):
                self.numRows = numRows
                self.numCols = numCols
                self.prevMove = ()
                self.point_count = 0
                self.turnNumber = 0
                self.board_raw = self.generateBoard()
                
                self.place = place(self)
                self.isValid = isValid(self)
                self.clear = clear(self)
                self.clearUtils = clearUtils(self)
                self.utils = boardUtils(self)
                self.points = points(self)
                self.shapeUtils = shapeUtils(self)
        
        def play(self, shape: Shape, pos):
                self.place.shape(shape, pos)


        def getTurnNumber(self):
                return self.turnNumber

        def getSize(self):
                return (self.numRows, self.numCols)
        
        def getBoard(self):
                return self.board
        
        def generateBoard(self):
                board = []
                for _ in range(self.numRows):
                        currRow = []
                        for _ in range(self.numCols):
                                currRow.append(False)
                        board.append(currRow)
                return board 
        

        def reset(self):
                self.board = self.generateBoard()
                self.points = 0
                self.turnNumber = 0
        


class boardUtils:
        def __init__(self, board: Board):
                self.board = board

        def printBoard(self):
                for _ in range(self.board.numCols + 2):
                        print("-", end = '   ')
                print()

                for row in self.board.getBoard():
                        print("|", end = '   ')
                        for unit in row:
                                print("X" if unit else ' ', end = '   ')
                        print("|")

                for _ in range(self.board.numCols + 2):
                        print("-", end = '   ')
                print()
                return 

class shapeUtils:
        def __init__(self, board: Board):
                self.board = board
        
        def getBlockPositions(shape: Shape, pos):
                positions = []
                target_row, target_col = pos

                for dR, dC in shape.getOffsets():
                        positions.append(target_row + dR, target_col + dC)
                
                return positions

class place:
        def __init__(self, board: Board):
                self.board = board
        
        def _activate(self, pos):
                row,col = pos
                self.board.board_raw[row][col] = True
        
        def block(self, pos):
                assert self.board.isValid.block(pos)
                self._activate(pos)

        def shape(self, shape, pos):
                assert self.board.isValid.shape(shape, pos)

                for curr_position in self.board.shapeUtils.getBlockPositions(shape, pos):
                        self._activate(curr_position)

                
class isValid:
        def __init__(self, board: Board):
                self.board = board
        
        def _isEmpty(self, pos):
                row, col = pos
                return self.board.board_raw[row][col] == False
        
        def block(self, pos):
                row, col = pos
                if (0 <= row < self.board.numRows) and (0 <= col < self.board.numCols):
                        if self._isEmpty(pos):
                                return True
                return False

        def shape(self, shape: Shape, pos):
                row, col = pos
                shape_height, shape_width = shape.getDims()

                # check if shape would even fit on the board at pos
                if (row + shape_height) > self.board.numRows - 1 or (col + shape_width) > self.board.numCols - 1:
                        return False

                # check if any positions are already filled
                for currPosition in self.board.shapeUtils.getBlockPositions(shape, pos):
                        if not self._isEmpty(currPosition):
                                return False
                        
                return True
        
        def getValidPositions(self, shape: Shape):
                possiblePositions = []
                for row in range(self.board.numRows):
                        for col in range(self.board.numCols):
                                currPos = (row, col)
                                if self.shape(shape, currPos):
                                        possiblePositions.append(currPos)

                return possiblePositions

class clear:
        def __init__(self, board: Board):
                self.board = board

        def check(self, last_played_move):
                cleared = 0
                colsCleared = []
                rowsCleared = []

                shape, pos = last_played_move

                blocks_pos = self.board.shapeUtils.getBlockPositions(shape, pos)
                for row, col in blocks_pos:
                        if (col not in colsCleared) and self.board.clearUtils.isColFull(col):
                                colsCleared.append(col)
                        if (row not in rowsCleared) and self.board.clearUtils.isRowFull(row):
                                rowsCleared.append(row)

                total_cleared = len(colsCleared) + len(rowsCleared)
                
                if total_cleared > 0:
                        points = (100 + 200*(cleared-1))
                else:
                        points = 0
                        
                return points
        
        def checkWithMask(self, shape, pos):
                colsCleared = []
                rowsCleared = []
                
                blocks_pos = self.board.shapeUtils.getBlockPositions(shape, pos)
                for row, col in blocks_pos:
                        if col not in colsCleared and self.board.clearUtils.isColFull_withMask(col, blocks_pos):
                                colsCleared.append(col)
                        if row not in rowsCleared and self.board.clearUtils.isRowFull_withMask(row, blocks_pos):
                                rowsCleared.append(row)
                
                total_cleared = len(colsCleared) + len(rowsCleared)
                if total_cleared > 0:
                        points = 100 + 200*(total_cleared-1)
                else:
                        points = 0

                return points
        
        def clearCol(self, col):
                for i in range(self.board.numRows):
                        self.board[i][col] = False
                return
        
        def clearRow(self, row):
                for i in range(self.board.numCols):
                        self.board[row][i] = False
                return

class clearUtils:
        def __init__(self, board: Board):
                self.board = board

        def isColFull(self, col):
                for i in range(self.board.numRows):
                        pos = (i,col)
                        if not self._checkPosition(pos):
                                return False
                return True

        def isColFull_withMask(self, col, shapeCoords):
                for i in range(self.board.numRows):
                        currPos = (i, col)
                        if not self._checkPosition(currPos) and currPos not in shapeCoords:
                                return False
                return True

        def isRowFull(self, row):
                for i in range(self.board.numCols):
                        pos = (row,i)
                        if not self._checkPosition(pos):
                                return False
                return True
        
        def isRowFull_withMask(self, row, shapeCoords):
                for i in range(self.numCols):
                        currPos = (row, i)
                        if not self._checkPosition(currPos) and currPos not in shapeCoords:
                                return False
                return True

        def _checkPosition(self, pos):
                row,col = pos
                return self.board.board_raw[row][col]

class points:
        def __init__(self, board: Board):
                self.board = board

        def add(self, pointsGained):
                self.board.points += pointsGained
        
        def get(self):
                return self.board.points