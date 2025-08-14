from Shape import Shape

class Action:
        def __init__(self, shape: Shape, row, col):
                self.shape = shape
                self.pos = (row, col)
                