from typing                 import TYPE_CHECKING
from QNet.GlobalActionIndex import GlobalActionIndex

if TYPE_CHECKING:
    from Game.Board.Board import Board

# ──────────────────────────────────────────────────────────────────────

class Agent:                
    def __init__(self, board: "Board"):
        self._board             = board
        self._shapes            = []
        self._gai = GlobalActionIndex()

