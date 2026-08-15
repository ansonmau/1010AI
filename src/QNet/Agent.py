from QNet.ExperienceReplay import ExperienceReplay
from QNet.GlobalActionIndex import GlobalActionIndex
from QNet.Qnet              import QNet
# ──────────────────────────────────────────────────────────────────────
import torch
import random
# ──────────────────────────────────────────────────────────────────────
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Game.Board.Board import Board
    from Game.Shape.Shape import Shape
# ──────────────────────────────────────────────────────────────────────

TARGET_NET_UPDATE_INTERVAL = 1000
EPSILON                    = 0.05

class Agent:                
    def __init__(self, board: "Board"):
        self._board          = board
        self._inventory      = []
        self._step_count     = 0

        self.inventory_size  = 3
        self.gai             = GlobalActionIndex()
        self.exp             = ExperienceReplay(1000)

        # must be after instantiating variables
        self._qnet           = QNet(self)
        self._target_network = QNet(self)


    # ╭────────────────────────────────────────────────╮
    # │                 qnet env tools                 │
    # ╰────────────────────────────────────────────────╯
    def reset(self):
        self._board.reset()
        self._step_count = 0
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

        self._step_count += 1
        return obs, reward, can_play, {}
    
    def update_target_net(self):
        if self._step_count % TARGET_NET_UPDATE_INTERVAL == 0:
            assert self._qnet is not None
            assert self._target_network is not None

            self._target_network.load_state_dict(self._qnet.state_dict())


    # ╭────────────────────────────────────────────────╮
    # │                  env helpers                   │
    # ╰────────────────────────────────────────────────╯
    def _observe_gamestate(self):
        return (self.get_inventory_tensor(), self.get_board_tensor())

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

    # ╭────────────────────────────────────────────────╮
    # │                   gai tools                    │
    # ╰────────────────────────────────────────────────╯
    def get_legal_gai_mask(self):
        mask = torch.zeros(self.gai.get_size())
        inv_shape_ids = self._get_inv_shape_ids()

        for i, gai_entry in self.gai.get_index():
            # gai_entry = (shape_id, row, col)
            if gai_entry[0] not in inv_shape_ids:
                mask[i] = False
            else:
                mask[i] = self._board.check.check_gai(gai_entry)

        return mask

    def _get_inv_shape_ids(self):
        return [s.get_id() for s in self._inventory]


    # ╭────────────────────────────────────────────────╮
    # │                  tensor tools                  │
    # ╰────────────────────────────────────────────────╯
    def get_inventory_tensor(self):
        inv_tensor = []
        for shape in self._inventory:
            inv_tensor.append(torch.tensor(shape.get_arr_repr(), dtype=torch.float32))
        return torch.stack(inv_tensor) # should be (3, 5, 5)

    def get_board_tensor(self):
        return torch.tensor(self._board.get_board(), dtype=torch.float32) # (1, 10, 10)

    # ╭────────────────────────────────────────────────╮
    # │                 training tools                 │
    # ╰────────────────────────────────────────────────╯
    def get_qvals(self):
        return self._qnet.forward()

    def get_target_qvals(self):
        return self._target_network.forward()

    def choose_move(self):
        assert self._qnet is not None

        move = None
        mask = self.get_legal_gai_mask()

        if random.random() < EPSILON:
            # locate 1's in the mask and convert from 2d (n,1) tensor to 1d (n) tensor
            legal_moves = torch.nonzero(mask).flatten()
            move = legal_moves[random.randrange(len(legal_moves))]
            move = move.item() # convert from tensor to value (int in this case)
        else:
            q_vals = self._qnet.forward().squeeze(0) # get rid of batch dim @ ind0 (1, gai_size) -> (gai_size)
            q_vals[mask==0] = float('-inf') # tensor feature
            move = q_vals.argmax().item()

        return move




