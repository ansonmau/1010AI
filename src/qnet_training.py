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

        self.episode_count  = 250
        self.epsilon        = 1
        self.batch_size     = 32

        self.stats = {
                "current_episode": {
                    "points":         0,
                    "last_reward":    0,
                    "total_reward":   0,
                    "steps":          0,
                    },
                "current_session": {
                    "episode_count": 0,
                    "steps":         0,
                    "highscore":          0,
                    "highscore_episode":  0,
                    "highreward":         0,
                    "highreward_episode": 0,
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
                self.agent.update_target_net() # only updates on preset number of steps

                self._update_episode_stats(reward)
                self._print_stats()

            self._update_session_stats()
            self._reset_episode_stats()

            epsilon = max(EPSILON_MIN, self.epsilon * EPSILON_DECAY)



    def _reset_episode_stats(self):
        curr_ep = self.stats["current_episode"]

        for key in curr_ep:
            curr_ep[key] = 0

    def _update_episode_stats(self, reward):
        curr_ep = self.stats["current_episode"]

        # points
        curr_ep["points"] = self.agent.get_points()
        
        # steps
        curr_ep["steps"] += 1

        # last reward
        curr_ep["last_reward"] = reward

        # total reward
        curr_ep["total_reward"] += reward

    def _update_session_stats(self):
        curr_ep = self.stats["current_episode"]
        curr_sesh = self.stats["current_session"]

        # highscore
        if curr_ep["points"] > curr_sesh["highscore"]:
            curr_sesh["highscore"] = curr_ep["points"]
            curr_sesh["highscore_episode"] = curr_sesh["episode_count"]

        # highreward
        if curr_ep["total_reward"] > curr_sesh["highreward"]:
            curr_sesh["highreward"] = curr_ep["total_reward"]
            curr_sesh["highreward_episode"] = curr_sesh["episode_count"]

        # steps
        curr_sesh["steps"] += curr_ep["steps"]

        # episode count
        curr_sesh["episode_count"] += 1

    def _print_stats(self):
        curr_ep = self.stats["current_episode"]
        curr_sesh = self.stats["current_session"]

        print("-- Episode -----")
        for key in curr_ep:
            print(f"{key}: {curr_ep[key]}")

        print("-- Session -----")
        for key in curr_sesh:
            print(f"{key}: {curr_sesh[key]}")

        self.agent.print_state()

def main():
    t = TTAI()
    t.run()
    print("Complete.")

if __name__ == "__main__":
    main()



