# ──────────────────────────────────────────────────────────────────────
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    pass
# ──────────────────────────────────────────────────────────────────────
import random
import torch 
from QNet.Agent import Agent, EPSILON_DECAY, EPSILON_MIN
from Game.Board.Board import Board
# ──────────────────────────────────────────────────────────────────────

def main():
    episode_count = 50
    board = Board(10,10)
    agent = Agent(board)
    epsilon = 1
    batch_size = 32

    for _ in range(episode_count):
        agent.reset()
        agent.print_state()
        while agent._can_play():
            state = agent._observe_gamestate()
            move = agent.choose_move(epsilon)
            next_state, reward, can_play, info = agent.step(move)
            agent.exp.save(state, move, reward, next_state, can_play)
            agent.training_step(batch_size)
            agent.update_target_net() # only updates every 1000 steps
            print(f"Turn number: {agent._step_count}")
            agent.print_state()
        epsilon = max(EPSILON_MIN, epsilon * EPSILON_DECAY)

if __name__ == "__main__":
    main()



