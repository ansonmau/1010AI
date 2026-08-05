from Game.Board.Board       import Board
from Game.Shape.Shape       import Shape
from QNet.AgentOld          import Agent
from QNet.GlobalActionIndex import GlobalActionIndex
from random                 import randrange

import torch
# ──────────────────────────────────────────────────────────────────────

def generateShapes(num):
        shapes = []
        for _ in range(num):
                shape_id = randrange(0, len(Shape.NAMES))
                shapes.append(Shape(shape_id))
        return shapes

def giveAgentShapes(agent: Agent):
        shapes = generateShapes(3)
        for shape in shapes:
            agent.addShape(shape)

def manual_play():
    board = Board(10,10)
    inventory = generateShapes(3)
    while len(inventory) > 0:
        print(f"Points: {board.get_point_count()}")
        print(f"Current shapes:")
        for i, s in enumerate(inventory):
            print(f"[{i}]: {s}")

        board.utils.printBoard()
        inp_shape = int(input("Enter shape: "))
        inp_row = int(input("Enter row #: ")) - 1
        inp_col = int(input("Enter col #: ")) - 1
        pos = (inp_row, inp_col)
        
        err = board.play_shape(inventory[inp_shape], pos)
        if err:
            print("Please try again")

def agent_play(): 
        startingShapes = generateShapes(3)

        b = Board(10,10)
        a = Agent(b)
        giveAgentShapes(a)
        while a.canPlay():
                b.utils.printBoard()
                shape, pos = a.selectShapeAndPosition()
                b.play_shape(shape, pos)
                a.removeShape(shape)
                print("Shapes left: {}".format([str(x) for x in a.get_shapes()]))
                print("Point total: {}".format(b.get_point_count()))
                print(''.join(["-" for _ in range(30)]))

                if not a.hasShapes():
                        giveAgentShapes(a)

        print("Game over. Points: {}".format(b.get_point_count()))
        return 

def qnet_play():
    b = Board(10,10)
    a = Agent(b)
    tensor_board = torch.tensor(b.get_board(), dtype=torch.float32)
    print(tensor_board)
    print(tensor_board.shape)
    print(tensor_board.dtype)

    s = Shape(1)
    print(s.get_arr_repr())

    # giveAgentShapes(a)
    #
    # while a.canPlay() and b.get_turn_count() < 5:
    #     b.utils.printBoard()
    #     shape, pos = a.selectShapeAndPosition()
    #     b.play_shape(shape, pos)
    #     a.removeShape(shape)
    #     print("Shapes left: {}".format([str(x) for x in a.get_shapes()]))
    #     print("Point total: {}".format(b.get_point_count()))
    #     print(''.join(["-" for _ in range(30)]))
    #
    #     if not a.hasShapes():
    #         giveAgentShapes(a)

    return 


# ──────────────────────────────────────────────────────────────────────

def main():
    qnet_play()


if __name__ == "__main__":
        main()
