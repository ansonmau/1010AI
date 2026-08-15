import enum
from QNet.ExperienceReplay import ExperienceReplay
from QNet.GlobalActionIndex import GlobalActionIndex
from QNet.Qnet              import QNet
from Game.Shape.Shape import Shape
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
# exploitation vs exploration
EPSILON_MIN                = 0.05
EPSILON_DECAY              = 0.995
# optimizer settings
LEARNING_RATE              = 0.001

class Agent:                
    def __init__(self, board: "Board"):
        self.gai             = GlobalActionIndex()
        self.exp             = ExperienceReplay(1000)

        self._board          = board
        self._step_count     = 0

        self.inventory_size  = 3
        self._inventory      = [Shape(0) for _ in range(self.inventory_size)]
        self._curr_inv_size = 3
        self._fill_inventory()

        # must be after instantiating variables
        self._qnet           = QNet(self)
        self._target_network = QNet(self)

        # must be after qnet
        self.optimizer = torch.optim.Adam(self._qnet.parameters(), lr=LEARNING_RATE)


    def play(self, shape, pos):
        assert shape.get_id() in self._get_inv_shape_ids()

        self._board.place.shape(shape, pos)
        # remove from inventory (replace with null shape)
        for i, s in enumerate(self._inventory):
            if shape.get_id() == s.get_id():
                self._inventory[i] = Shape.get_null_shape()
                self._curr_inv_size -= 1
        
        # fill inventory if empty
        if self._curr_inv_size == 0:
            self._fill_inventory()
            self._curr_inv_size = self.inventory_size

    def print_state(self):
        self._board.utils.printBoard()
        inv = [str(s) for s in self._inventory]
        for i,n in enumerate(inv):
            print(f"{i}: {n}")


    def _fill_inventory(self):
        for i in range(self.inventory_size):
            self._inventory[i] = Shape.get_random_shape()

    # ╭────────────────────────────────────────────────╮
    # │                 qnet env tools                 │
    # ╰────────────────────────────────────────────────╯
    def reset(self):
        self._board.reset()
        self._step_count = 0
        self._fill_inventory()
        return self._observe_gamestate()

    def step(self, chosen_index):
        shape_id, row, col = self.gai.get(chosen_index)

        s = Shape(shape_id)
        pos = (row,col)

        self.play(s, pos)

        # get updated info
        obs      = self._observe_gamestate()
        can_play = self._can_play()
        reward   = self._calc_reward()

        self._step_count += 1
        return obs, reward, can_play, {"gai_move": self.gai.get(chosen_index)}
    
    def update_target_net(self):
        if self._step_count % TARGET_NET_UPDATE_INTERVAL == 0:
            assert self._qnet is not None
            assert self._target_network is not None

            self._target_network.load_state_dict(self._qnet.state_dict())


    # ╭────────────────────────────────────────────────╮
    # │                  env helpers                   │
    # ╰────────────────────────────────────────────────╯
    def _observe_gamestate(self):
        return (self.get_board_tensor().unsqueeze(0), self.get_inventory_tensor())

    def _can_play(self):
        for shape in self._inventory:
            if len(self._board.check.get_all_valid_positions(shape)) > 0:
                return True
        return False

    def _calc_reward(self):
        reward = 0

        factors = {
                # points = (100 + 200*(total_cleared-1))
                "points gained": self._board.get_point_diff(),
                "loss penalty": 0 if self._can_play() else -200,
                }
        
        for v in factors.values():
            reward += int(v)

        return reward

    # ╭────────────────────────────────────────────────╮
    # │                   gai tools                    │
    # ╰────────────────────────────────────────────────╯
    def get_legal_gai_mask(self):
        mask = torch.zeros(self.gai.get_size())
        inv_shape_ids = self._get_inv_shape_ids()

        for i, gai_entry in enumerate(self.gai.get_index()):
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
    def get_qvals(self, board_tensor=None, inv_tensor=None):
        return self._qnet.forward(board_tensor=board_tensor, inv_tensor=inv_tensor)

    def get_target_qvals(self, board_batch, inv_batch):
        return self._target_network.forward(board_tensor=board_batch, inv_tensor=inv_batch)

    def choose_move(self, epsilon):
        assert self._qnet is not None

        move = None
        mask = self.get_legal_gai_mask()

        if random.random() < epsilon:
            # locate 1's in the mask and convert from 2d (n,1) tensor to 1d (n) tensor
            legal_moves = torch.nonzero(mask).flatten()
            move = legal_moves[random.randrange(len(legal_moves))]
            move = move.item() # convert from tensor to value (int in this case)
        else:
            q_vals = self.get_qvals().squeeze(0) # get rid of batch dim @ ind0 (1, gai_size) -> (gai_size)
            q_vals[mask==0] = float('-inf') # tensor feature
            move = q_vals.argmax().item()

        return move



    def training_step(self, batch_size, discount=0.99):
        if self.exp.get_size() < batch_size:
            # not enough experience
            return

        # ─────────────────────────< pull up experience >─────────────────────────
        # get samples
        states, actions, rewards, next_states, can_plays = self.exp.sample(batch_size)

        # turn samples into tensors (batches)

        # states: (board_tensor, inv_tensor)
        # current board + pieces batches
        b_board = torch.stack([s[0] for s in states])
        b_pieces = torch.stack([s[1] for s in states])

        # next board + pieces batches
        next_b_board = torch.stack([s[0] for s in next_states])
        next_b_pieces = torch.stack([s[1] for s in next_states])

        # others
        t_rewards = torch.tensor(rewards, dtype=torch.float32)
        t_can_plays = torch.tensor(can_plays, dtype=torch.float32)
        t_actions = torch.tensor(actions)

        # ───────────────────< compare live and target qvals >─────────────────

        # get q values for the specific actions taken
        # - qvals are returned in a (32, gai_size) batch, we want values from the 1st dimension
        # - must match actions tensor to qval tensor dimensions
        all_live_qvals = self.get_qvals(b_board, b_pieces)
        predicted_qvals = all_live_qvals.gather(1, t_actions.unsqueeze(0)).squeeze(1) # turn back into 1d list 


        # get target qvals and plug them into bellman eq to get predicted "correct" qvals
        # - no_grad() tells torch to not use this for backpropogration (save space and comp)
        with torch.no_grad():
            next_qvals = self.get_target_qvals(next_b_board, next_b_pieces)
            best_qval = next_qvals.max(dim=1).values # (32, gai_size)
            target_qvals = t_rewards + discount * best_qval * (1 - t_can_plays) # bellman eq (element-wise ops)

        # calc mean squared error (loss)
        loss = torch.nn.functional.mse_loss(predicted_qvals, target_qvals)
        
        # ──────────────< backpropogate and update qnet weightings >──────────────
        self.optimizer.zero_grad() # clear history
        loss.backward()             # backpropogate
        self.optimizer.step()      # update weights


