import random
import torch 

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Game.Board.Board import Board
    from QNet.Agent import Agent


def training_step(agent: "Agent", batch_size, discount):
    if agent.exp.get_size() < batch_size:
        # not enough experience
        return

    # ─────────────────────────< pull up experience >─────────────────────────
    # get samples
    states, actions, rewards, next_states, can_plays = agent.exp.sample(batch_size)

    # turn samples into tensors (batches)

    # states: (inv_tensor, board_tensor)
    # current board + pieces batches
    b_board = torch.stack([s[1] for s in states])
    b_pieces = torch.stack([s[0] for s in states])

    # next board + pieces batches
    next_b_board = torch.stack([s[1] for s in next_states])
    next_b_pieces = torch.stack([s[0] for s in next_states])

    # others
    t_rewards = torch.tensor(rewards, dtype=torch.float32)
    t_can_plays = torch.tensor(can_plays, dtype=torch.float32)
    t_actions = torch.tensor(actions)

    # ───────────────────< compare live and target qvals >─────────────────
    live_qvals = agent.get_qvals()
    predicted_qvals = live_qvals.gather(1, t_actions.unsqueeze(1)).squeeze(1)
    target_qvals = agent.get_target_qvals()






