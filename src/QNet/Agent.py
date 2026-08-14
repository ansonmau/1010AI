from QNet.GlobalActionIndex import GlobalActionIndex
# ──────────────────────────────────────────────────────────────────────
import torch
# ──────────────────────────────────────────────────────────────────────
from typing                 import TYPE_CHECKING
if TYPE_CHECKING:
    from Game.Board.Board import Board
    from Game.Shape.Shape import Shape
# ──────────────────────────────────────────────────────────────────────

class Agent:                
    def __init__(self, board: "Board"):
        self._board         = board
        self._inventory     = []

        self.gai            = GlobalActionIndex()
        self.inventory_size = 3

    def reset(self):
        self._board.reset()
        return self._observe_gamestate()

    def step(self, chosen_index):
        shape_id, row, col = self.gai.get(chosen_index)

        s = Shape(shape_id)
        pos = (row,col)

        self._board.place.shape(s, pos)

        # get updated info
        obs      = self._observe_gamestate()
        can_play = self._can_play()
        reward   = self._calc_reward()

        return obs, reward, can_play, {}


    def get_legal_gai_mask(self):
        mask = torch.zeros(self.gai.get_size())

        for i, gai_entry in self.gai.get_index():
            mask[i] = self._board.check.check_gai(gai_entry)

        return mask

    def get_inventory_tensor(self):
        inv_tensor = []
        for shape in self._inventory:
            inv_tensor.append(torch.tensor(shape.get_arr_repr(), dtype=torch.float32))
        return torch.stack(inv_tensor) # should be (3, 5, 5)

    def get_board_tensor(self):
        return torch.tensor(self._board.get_board(), dtype=torch.float32) # (1, 10, 10)

    # ── step helpers ──────────────────────────────────────────────────────
    def _observe_gamestate(self):
        return self.get_inventory_tensor(), self.get_board_tensor()

    def _can_play(self):
        for shape in self._inventory:
            if len(self._board.check.get_all_valid_positions(shape)) == 0:
                return False 
        return True

    def _calc_reward(self):
        reward = 0

        factors = {
                # points = (100 + 200*(total_cleared-1))
                "points gained": self._board.get_point_diff(),
                "loss penalty": 0 if self._can_play() else -200,
                }
        
        for k,v in factors:
            reward += int(v)

        return reward




