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
class TTAI:
    def __init__(self):
        self.board = Board(10,10)
        self.agent = Agent(self.board)

        self.episode_count  = 2500
        self.epsilon        = 1
        self.batch_size     = 64

        self.stats = {
                "current_episode": {
                    "points":               0,
                    "last_reward":          0,
                    "total_reward":         0,
                    "steps":                0,
                    "board_fill_ratio":     0,
                    },
                "current_session": {
                    "episode_count":        0,
                    "total_steps":          0,
                    "total_reward":         0,
                    "high_score":           0,
                    "high_reward":          0,
                    "high_score_episode":   0,
                    "high_reward_episode":  0,
                    "average_steps":        0,
                    "average_total_reward": 0,
                    "epsilon":              float(0),
                    },
                }

    def run(self):
        for curr_episode in range(self.episode_count):
            self.agent.reset()
            self.agent.print_state()

            while self.agent._can_play():
                state = self.agent._observe_gamestate()
                move = self.agent.choose_move(self.epsilon)
                next_state, reward, can_play, info = self.agent.step(move)
                self.agent.exp.save(state, move, reward, next_state, can_play)
                self.agent.training_step(self.batch_size)
                self.agent.update_target_net(800) # default 500

                self._update_episode_stats(reward)
                self._print_stats()

            self.epsilon = max(EPSILON_MIN, self.epsilon * EPSILON_DECAY)

            self._update_session_stats()
            self._reset_episode_stats()

    # ╭────────────────────────────────────────────────╮
    # │                    helpers                     │
    # ╰────────────────────────────────────────────────╯

    def _reset_episode_stats(self):
        curr_ep = self.stats["current_episode"]

        for key in curr_ep:
            curr_ep[key] = 0

    def _update_episode_stats(self, reward):
        curr_ep = self.stats["current_episode"]

        curr_ep["points"] = self.agent.get_points()
        curr_ep["steps"] += 1
        curr_ep["last_reward"] = reward
        curr_ep["total_reward"] += reward
        curr_ep["board_fill_ratio"] = self.agent._board.get_filled_ratio() 

    def _update_session_stats(self):
        curr_ep = self.stats["current_episode"]
        curr_sesh = self.stats["current_session"]

        curr_sesh["total_steps"]   += curr_ep["steps"]
        curr_sesh["total_reward"]  += curr_ep["total_reward"]
        curr_sesh["episode_count"] += 1
        curr_sesh["epsilon"]        = round(self.epsilon, 5)

        # ── High ─────────────────────────────────────────────────────────────
        # score
        if curr_ep["points"] > curr_sesh["high_score"]:
            curr_sesh["high_score"] = curr_ep["points"]
            curr_sesh["high_score_episode"] = curr_sesh["episode_count"]

        # reward
        if curr_ep["total_reward"] > curr_sesh["high_reward"]:
            curr_sesh["high_reward"] = curr_ep["total_reward"]
            curr_sesh["high_reward_episode"] = curr_sesh["episode_count"]

        # ── Avgs ──────────────────────────────────────────────────────────────
        # steps
        curr_sesh["average_steps"] = int(curr_sesh["total_steps"] / curr_sesh["episode_count"])

        # reward - total
        curr_sesh["average_total_reward"] = int(curr_sesh["total_reward"] / curr_sesh["episode_count"])



    def _print_stats(self):
        curr_ep = self.stats["current_episode"]
        curr_sesh = self.stats["current_session"]

        print("-- Session -----")
        for key in curr_sesh:
            print(f"{key}: {curr_sesh[key]}")

        print("-- Episode -----")
        for key in curr_ep:
            print(f"{key}: {curr_ep[key]}")

        self.agent.print_state()

        print("=" * 15)

def main():
    t = TTAI()
    t.run()
    print("Complete.")

if __name__ == "__main__":
    main()



