# ──────────────────────────────────────────────────────────────────────
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass
# ──────────────────────────────────────────────────────────────────────
import os
import random
import torch 
from QNet.Agent       import Agent, EPSILON_DECAY, EPSILON_MIN
from QNet.Checkpoint  import Checkpoint
from Game.Board.Board import Board
from Ui.stats         import StatTrak
# ──────────────────────────────────────────────────────────────────────

AVERAGES_WINDOW_SIZE = 100

class TTAI:
    def __init__(self):
        self.episode_count = 100000
        self.batch_size    = 256
        self.greedy_freq   = 100
        self.epsilon       = 1
        self.save_freq     = 50
        self.upload_freq   = 100

        self.board = Board(10,10)
        self.agent = Agent(self.board)
        self.st    = StatTrak(self.episode_count, AVERAGES_WINDOW_SIZE)
        self.chk = Checkpoint()


    def run(self):
        for curr_episode in range(self.episode_count):
            def on(freq):
                return curr_episode % freq == 0

            self.agent.reset()
            self.st.new_episode()

            if on(self.greedy_freq):
                cEps = 0
            else:
                cEps = self.epsilon

            if on(self.save_freq):
                qs, os = self.agent.get_save_states()
                self.chk.update({
                    "qnet_state": qs,
                    "optimizer_state": os,
                    "stats": self.st.get_save_data(),
                    "ep": curr_episode,
                    })
                self.chk.save("9")
            
            if on(self.upload_freq):
                self.chk.upload()

            self.st.update({
                "type": "session",
                "epsilon": cEps,
                })


            x = cEps==0
            while self.agent._can_play():
                # ── agent loop ────────────────────────────────────────────────────────nlucky sequenc
                state = self.agent._observe_gamestate()
                move = self.agent.choose_move(cEps)
                next_state, reward, can_play, info = self.agent.step(move)
                self.agent.exp.save(state, move, reward, next_state, can_play)
                self.agent.training_step(self.batch_size)
                self.agent.update_target_net() 

                # ── update stats ──────────────────────────────────────────────────────nlucky sequenc
                ep_data = {
                        "type":             "episode",
                        "reward":           reward,
                        "reward_list":      info["reward_list"],
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



