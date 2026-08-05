from Game.Board.Board import Board
from Game.Shape.Shape import Shape


DEFAULT_NUM_ROWS = 10
DEFAULT_NUM_COLS = 10

class GlobalActionIndex:
    def __init__(self):
        self._index = []
        self._shape_slices = {}
        self._tuple_to_action = {}

        self.__generate_index()

    def print(self):
        print(f"{self._index}")
        print(f"{self._shape_slices}")
        print(f"{self._tuple_to_action}")

    def __generate_index(self):
            """
            generates all possible moves (global action index)

            global action index [list] -> all possible moves in the game
            tuple to action [dict]     -> gives index of a tuple in the gai
            action index slices [dict] -> dict that gives the index range of a
            specific shape's possible moves in the gai
            """

            temp_board = Board(DEFAULT_NUM_ROWS, DEFAULT_NUM_COLS)
            all_shape_ids = Shape.PATTERNS.keys()

            for shapeID in all_shape_ids:
                shapeStartIndex = len(self._index)  # for shape ranges

                for valid_position in temp_board.check.get_all_valid_positions(Shape(shapeID)):
                    # given an empty board, valid positions should be all positions that aren't impossible
                    x_pos, y_pos = valid_position
                    currTuple = (shapeID, x_pos, y_pos)
                    self._index.append(currTuple)

                    currIndex = len(self._index) - 1
                    self._tuple_to_action[currTuple] = currIndex
                                    
                shapeEndIndex = len(self._index)

