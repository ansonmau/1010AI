from Board import Board
from Shape import Shape, SHAPENAME_TO_ID
from Agent import Agent
from random import randrange

def testPlace(board : Board, shapeName, row, col):
        pos = (row, col)
        currShape = Shape(shapeName)
        currShape.setPos(pos)
        possiblePos = board.getPossiblePositions(currShape)

        print("possible positions for '{}': {}".format(currShape, possiblePos))
        print("Placing '{}' at {}".format(currShape, currShape.getPos()), end = '...')
        if board.placeShape(currShape):
                print("success")
                print("points: {}".format(board.getPoints()))
        else:
                print("failed")
        print("Board: (turn {})".format(board.getTurnNumber()))
        board.printBoard()

def generateShapes(num):
        shapes = []
        shapeNames = SHAPENAME_TO_ID.keys()
        shapeNames = list(shapeNames)
        for _ in range(num):
                i = randrange(0, len(shapeNames))
                newShape = Shape(shapeNames[i])
                shapes.append(newShape)
        return shapes

def main(): 
        startingShapes = generateShapes(3)

        b = Board(10,10)
        a = Agent(b, startingShapes)
        while a.canPlay():
                b.printBoard()
                print("Shapes left: {}".format([str(x) for x in a.shapes]))
                print("Playable shapes: {}".format([str(x) for x in a.getPlayableShapes()]))

                a.selectShapeAndPosition()

                print("Selected shape: {}".format(a.selectedShape))
                print("Selected position: {}".format(a.selectedPosition))
                print("Potential points: {}".format(b.potentialPoints(a.selectedShape, a.selectedPosition)))

                b.placeShape(a.selectedShape, a.selectedPosition)

                a.removeShape(a.selectedShape)

                print("Point total: {}".format(b.getPoints()))
                print(''.join(["-" for _ in range(30)]))

                if not a.hasShapes():
                        for shape in generateShapes(3):
                                a.addShape(shape)

        print("Game over. Points: {}".format(b.getPoints()))

        return 


if __name__ == "__main__":
        main()