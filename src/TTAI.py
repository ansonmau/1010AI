# ──────────────────────────────────────────────────────────────────────
from collections import deque
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass
# ──────────────────────────────────────────────────────────────────────
import random
import torch 
from QNet.Agent import Agent, EPSILON_DECAY, EPSILON_MIN
from Game.Board.Board import Board
from Ui.stats import StatTrak
# ──────────────────────────────────────────────────────────────────────

AVERAGES_WINDOW_SIZE = 100

class TTAI:
    def __init__(self):
        self.board = Board(10,10)
        self.agent = Agent(self.board)

        # self.agent._reward_calculator.enable_print_rewards()

        self.episode_count = 10000
        self.epsilon       = 1
        self.batch_size    = 128
        self.greedy_freq   = 100
        self.st            = StatTrak(self.episode_count, AVERAGES_WINDOW_SIZE)


    def run(self):
        for curr_episode in range(self.episode_count):
            self.agent.reset()
            self.st.new_episode()

            greedy = (curr_episode % self.greedy_freq == 0)
            cEps = 0 if greedy else self.epsilon

            sesh_data = {
                    "type": "session",
                    "epsilon": cEps,
                    }
            self.st.update(sesh_data)

            while self.agent._can_play():
                # ── agent loop ────────────────────────────────────────────────────────
                state = self.agent._observe_gamestate()
                move = self.agent.choose_move(cEps)
                next_state, reward, can_play, info = self.agent.step(move)
                self.agent.exp.save(state, move, reward, next_state, can_play)
                self.agent.training_step(self.batch_size)
                self.agent.update_target_net() 

                # ── update stats ──────────────────────────────────────────────────────
                ep_data = {
                        "type":             "episode",
                        "reward":           reward,
                        "can_play":         can_play,
                        "move":             move,
                        "board_fill_ratio": self.board.utils.get_filled_ratio(),
                        "points":           self.board.get_point_diff(),
                        "loss":             info["loss"],
                        }
                self.st.update(ep_data)

                # ── display ───────────────────────────────────────────────────────────
                print(self.st.get_str())
                self.agent.print_state()

            self.epsilon = max(EPSILON_MIN, self.epsilon * EPSILON_DECAY)


def main():
    t = TTAI()
    t.run()
    print("Complete.")

if __name__ == "__main__":
    main()



