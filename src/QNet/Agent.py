from QNet.GlobalActionIndex import GlobalActionIndex
# ──────────────────────────────────────────────────────────────────────
import torch
# ──────────────────────────────────────────────────────────────────────
from typing                 import TYPE_CHECKING
if TYPE_CHECKING:
    from Game.Board.Board import Board
# ──────────────────────────────────────────────────────────────────────

class Agent:                
    def __init__(self, board: "Board"):
        self._board         = board
        self._inventory     = []

        self.gai            = GlobalActionIndex()
        self.inventory_size = 3


    def get_inventory_tensor(self):
        inv_tensor = []
        for shape in self._inventory:
            inv_tensor.append(torch.tensor(shape.get_arr_repr(), dtype=torch.float32))
        return torch.stack(inv_tensor) # should be (3, 5, 5)

    def get_board_tensor(self):
        return torch.tensor(self._board.get_board(), dtype=torch.float32) # (1, 10, 10)
        
