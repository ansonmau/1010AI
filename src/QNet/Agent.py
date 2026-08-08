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
        self._board             = board
        self._inventory            = []
        self._gai = GlobalActionIndex()

        self._tensor_board = torch.tensor(self._board.get_board(), dtype=torch.float32)
        
    def _generate_inventory_tensor
