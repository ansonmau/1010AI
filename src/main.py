from Game.Board.Board import Board
from Game.Shape.Shape import Shape, SHAPENAMES, initialize_shape_data
from QNet.Agent import Agent
from random import randrange

def generateShapes(num):
        shapes = []
        for _ in range(num):
                shape_id = randrange(0, len(SHAPENAMES))
                shapes.append(Shape(shape_id))
        return shapes

def giveAgentShapes(agent: Agent):
        shapes = generateShapes(3)
        agent.addShapes(shapes)

def main1(): 
        initialize_shape_data()
        startingShapes = generateShapes(3)

        b = Board(10,10)
        a = Agent(b)
        giveAgentShapes(a)
        while a.canPlay():
                b.utils.printBoard()
                a.play()
                print("Shapes left: {}".format([str(x) for x in a.shapes]))


                print("Point total: {}".format(b.points.get()))
                print(''.join(["-" for _ in range(30)]))

                if not a.hasShapes():
                        giveAgentShapes(a)

        print("Game over. Points: {}".format(b.points.get()))

        return 

def main():
    b = Board(10,10)
    b.utils.printBoard()

if __name__ == "__main__":
        main()
