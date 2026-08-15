from Game.Shape.Shape import Shape
import random

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Game.Board.Board import Board

class Agent:                
        def __init__(self, board: "Board"):
                self._board             = board
                self._shapes            = []
                self._selectedShape     = None
                self._possiblePositions = []
                self._selectedPosition  = ()

        def canPlay(self):
            return True if len(self.getPlayableShapes()) > 0 else False

        def hasShapes(self):
                return True if len(self._shapes) > 0 else False

        def addShape(self, shape):
                self._shapes.append(shape)
        
        def removeShape(self, shape):
                self._shapes.remove(shape)

        def get_shapes(self):
            return self._shapes
        
        def selectShapeAndPosition(self):
            assert self.hasShapes()

            playableShapes = self.getPlayableShapes()

            assert len(playableShapes) > 0

            bestMoves = self.getBestMoves(playableShapes)
            
            assert len(bestMoves) > 0

            selectedIndex = 0
            if len(bestMoves) > 1:
                    selectedIndex = random.randrange(0, len(bestMoves))
            
            self._selectedShape = bestMoves[selectedIndex][0]
            self._selectedPosition = bestMoves[selectedIndex][1]

            return self._selectedShape, self._selectedPosition


        def getBestMoves(self, playableShapes):
                highestPotential = -float("inf")
                bestMoves = []

                for currShape in playableShapes:
                        for possiblePosition in self._board.check.get_all_valid_positions(currShape):
                                currMovePotential, _, _ = self._board.clear.simulate(currShape, possiblePosition)
                                
                                if currMovePotential > highestPotential:
                                        highestPotential = currMovePotential
                                        bestMoves.clear()
                                        bestMoves.append((currShape, possiblePosition))
                                elif currMovePotential == highestPotential:
                                        bestMoves.append((currShape, possiblePosition))

                # print("Best moves ({}): {}".format(highestPotential, [(str(x),y) for x,y in bestMoves]))
                return bestMoves

        def getPlayableShapes(self):
                assert len(self._shapes) > 0

                playable = []

                for shape in self._shapes:
                        possiblePositions = self._board.check.get_all_valid_positions(shape)
                        if len(possiblePositions) > 0:
                                playable.append(shape)
                
                return playable

        def calcPossiblePositions(self):
                assert self._selectedShape is not None
                self._possiblePositions = self._board.check.get_all_valid_positions(self._selectedShape)

        def selectPosition(self):
                assert self._selectedShape is not None
                selectedPos = random.randrange(0, len(self._possiblePositions))
                self._selectedPosition = self._possiblePositions[selectedPos]
                self._selectedShape.setPos(self._selectedPosition)
