from Shape import Shape

class Board:
        def __init__(self, numRows, numCols):
                self.numRows = numRows
                self.numCols = numCols
                self.prevMove = ()
                self.points = 0
                self.turnNumber = 0
                self.board = self._generateBoard()
                pass
        
        def getEmptyBoard(self):
                return Board(self.numRows, self.numCols)

        def getTurnNumber(self):
                return self.turnNumber

        def getSize(self):
                return (self.numRows, self.numCols)
        
        def _generateBoard(self):
                board = []
                for _ in range(self.numRows):
                        currRow = []
                        for _ in range(self.numCols):
                                currRow.append(False)
                        board.append(currRow)
                return board 
        
        def getBoard(self):
                return self.board
        
        def reset(self):
                self.board = self._generateBoard()
                self.lastPlacedShape = None
                self.points = 0
                self.turnNumber = 0
        
        def printBoard(self):
                for col in range(self.numCols + 2):
                        print("-", end = '   ')
                print()

                for row in self.board:
                        print("|", end = '   ')
                        for unit in row:
                                print("X" if unit else ' ', end = '   ')
                        print("|")

                for col in range(self.numCols + 2):
                        print("-", end = '   ')
                print()
                return
        
        def placeShape(self, shape: Shape, pos):
                if self.canPlaceShape(shape, pos):
                        for position in self.getShapeCoords(shape, pos):
                                self.place(position)
                        self.prevMove = (shape, pos)
                        self.checkClear()
                        self.turnNumber += 1
                        return True
                
                return False


        def place(self, pos):
                row, col = pos
                if self.canPlace(pos):
                        self.board[row][col] = True
                        return True
                return False

                # try:
                #         self.board[row][col] = True
                #         return True
                # except:
                #         return False
        

        
        def checkClear(self):
                cleared = 0
                colsCleared = []
                rowsCleared = []

                for row, col in self.getShapeCoords(*self.prevMove):
                        if (col not in colsCleared) and self._checkColClear(col):
                                cleared += 1
                                colsCleared.append(col)
                        if (row not in rowsCleared) and self._checkRowClear(row):
                                cleared += 1
                                rowsCleared.append(row)
                
                if cleared > 0:
                        for col in colsCleared:
                                self._clearCol(col)
                        for row in rowsCleared:
                                self._clearRow(row)

                        self.addPoints(100 + 200*(cleared-1))
                        
                return
        
        def potentialPoints(self, shape: Shape, pos):
                cleared = 0
                colsCleared = []
                rowsCleared = []
                points = 0

                shapeCoords = self.getShapeCoords(shape, pos)

                for row,col in shapeCoords:
                        if (col not in colsCleared) and self._checkColClearGhost(col, shapeCoords):
                                cleared += 1
                                colsCleared.append(col)
                        if (row not in rowsCleared) and self._checkRowClearGhost(row, shapeCoords):
                                cleared += 1
                                rowsCleared.append(row)
                
                if cleared > 0:
                        points += 100 + 200*(cleared-1)

                return points 

        def _checkColClear(self, col):
                for i in range(self.numRows):
                        if not self.board[i][col]:
                                return False
                return True

        def _checkColClearGhost(self, col, shapeCoords):
                for i in range(self.numRows):
                        currPos = (i, col)
                        if not self.board[i][col] and currPos not in shapeCoords:
                                return False
                return True

        def _checkRowClear(self, row):
                for i in range(self.numCols):
                        if not self.board[row][i]:
                                return False
                return True
        
        def _checkRowClearGhost(self, row, shapeCoords):
                for i in range(self.numCols):
                        currPos = (row, i)
                        if not self.board[row][i] and currPos not in shapeCoords:
                                return False
                return True
        
        def _clearCol(self, col):
                for i in range(self.numRows):
                        self.board[i][col] = False
                return
        
        def _clearRow(self, row):
                for i in range(self.numCols):
                        self.board[row][i] = False
                return

        def addPoints(self, pointsGained):
                self.points += pointsGained
        
        def getPoints(self):
                return self.points
        
        def canPlace(self, pos):
                row, col = pos
                if (0 <= row < self.numRows) and (0 <= col < self.numCols):
                        if not self.board[row][col]:
                                return True
                return False

        def canPlaceShape(self, shape: Shape, pos):
                row, col = pos
                shapeH, shapeW = shape.getDims()

                if (row+shapeH) > self.numRows - 1 or (col+shapeW) > self.numCols - 1:
                        return False

                for currPosition in self.getShapeCoords(shape, pos):
                        if not self.canPlace(currPosition):
                                return False
                        
                return True

        def getPossiblePositions(self, shape: Shape):
                possiblePositions = []
                for row in range(self.numRows):
                        for col in range(self.numCols):
                                currPos = (row, col)
                                if self.canPlaceShape(shape, currPos):
                                        possiblePositions.append(currPos)

                return possiblePositions

        def getShapeCoords(self, shape: Shape, pos):
                row,col = pos
                coords = []
                offsets = shape.getOffsets()

                for dr, dc in offsets:
                        coords.append((row+dr, col+dc))
                
                return coords

                
        