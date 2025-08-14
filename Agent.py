from Board import Board
from Shape import Shape, SHAPE_PATTERNS
import random

class Agent:                
        def __init__(self, board: Board, shapes):
                self.board = board
                
                self.shapes = shapes
                self.selectedShape = None

                self.possiblePositions = []
                self.selectedPosition = ()

                self.globalActionIndex = []
                self.tupleToAction = {}
                self.actionIndexSlices = {}

                self.createGlobalActionIndex()

        def setBoard(self, board):
                self.board = board

        def hasShapes(self):
                return True if len(self.shapes) > 0 else False

        def addShape(self, shape):
                self.shapes.append(shape)
        
        def removeShape(self, shape):
                self.shapes.remove(shape)
        
        def selectShapeAndPosition(self):
                assert self.hasShapes()

                playableShapes = self.getPlayableShapes()

                assert len(playableShapes) > 0

                bestMoves = self.getBestMoves(playableShapes)
                
                assert len(bestMoves) > 0

                selectedIndex = 0
                if len(bestMoves) > 1:
                        selectedIndex = random.randrange(0, len(bestMoves))
                
                self.selectedShape = bestMoves[selectedIndex][0]
                self.selectedPosition = bestMoves[selectedIndex][1]

        def getBestMoves(self, playableShapes):
                highestPotential = -float("inf")
                bestMoves = []

                for currShape in playableShapes:
                        for possiblePosition in self.board.getPossiblePositions(currShape):
                                currMovePotential = self.board.potentialPoints(currShape, possiblePosition)
                                
                                if currMovePotential > highestPotential:
                                        highestPotential = currMovePotential
                                        bestMoves.clear()
                                        bestMoves.append((currShape, possiblePosition))
                                elif currMovePotential == highestPotential:
                                        bestMoves.append((currShape, possiblePosition))

                # print("Best moves ({}): {}".format(highestPotential, [(str(x),y) for x,y in bestMoves]))
                return bestMoves

        def canPlay(self):
                return True if len(self.getPlayableShapes()) > 0 else False

        def getPlayableShapes(self):
                assert len(self.shapes) > 0

                playable = []

                for shape in self.shapes:
                        possiblePositions = self.board.getPossiblePositions(shape)
                        if len(possiblePositions) > 0:
                                playable.append(shape)
                
                return playable

        def calcPossiblePositions(self):
                assert self.selectedShape is not None
                self.possiblePositions = self.board.getPossiblePositions(self.selectedShape)

        def selectPosition(self):
                selectedPos = random.randrange(0, len(self.possiblePositions))
                self.selectedPosition = self.possiblePositions[selectedPos]
                self.selectedShape.setPos(*self.selectedPosition)

        def createGlobalActionIndex(self):
                self.globalActionIndex = []
                self.tupleToAction = {}
                self.actionIndexSlices = {}

                shapeIDs = SHAPE_PATTERNS.keys()
                shapeIDs = sorted(shapeIDs)
                
                for shapeID in shapeIDs:
                        currShape = Shape.createFromID(shapeID)
                        shapeStartIndex = len(self.globalActionIndex)

                        for vRow, vCol in self._getValidPositions(currShape):
                                currTuple = (shapeID, vRow, vCol)
                                self.globalActionIndex.append(currTuple)

                                currIndex = len(self.globalActionIndex) - 1
                                self.tupleToAction[currTuple] = currIndex
                                            
                        shapeEndIndex = len(self.globalActionIndex) - 1
                        self.actionIndexSlices[shapeID] = (shapeStartIndex, shapeEndIndex)
        
        def _getValidPositions(self, shape: Shape):
                nRows, nCols = self.board.getSize()
                validPositions = []

                # all shapes anchored top left
                for row in range(nRows):
                        for col in range(nCols):
                                # check if shape size is within bounds of game
                                # only have to worry about it being too large

                                sHeight, sWidth = shape.getDims()
                                heightExt = sHeight - 1
                                widthExt = sWidth - 1
                                if ((row + heightExt) <= nRows-1) and ((col + widthExt) <= nCols-1):
                                        validPositions.append((row, col))
                
                return validPositions

                        