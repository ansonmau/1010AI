from Board import Board
from Shape import Shape, SHAPENAME_TO_ID, SHAPE_PATTERNS
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

                numRows, numCols = self.board.getSize()
                
                emptyBoard = self.board.getEmptyBoard()
                
                for shapeID in shapeIDs:
                        currShape = Shape.createFromID(shapeID)
                        shapeStartIndex = len(self.globalActionIndex)
                        for row in range(numRows):
                                for col in range(numCols):
                                        currPos = (row,col)
                                        if emptyBoard.canPlaceShape(currShape, currPos):
                                                currTuple = (shapeID, row, col)
                                                currIndex = len(self.globalActionIndex)

                                                self.globalActionIndex.append(currTuple)
                                                self.tupleToAction[currTuple] = currIndex                
                        shapeEndIndex = len(self.globalActionIndex)
                        self.actionIndexSlices[shapeID] = (shapeStartIndex, shapeEndIndex)
                        

                