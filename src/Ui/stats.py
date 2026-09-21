from collections import deque

DECIMAL_CUTOFF = 2

class StatTrak:
    def __init__(self, total_episode_count, avgs_size=100):
        self._data_log = deque(maxlen=avgs_size)
        self._loss_log = []


        self.d_reward_list = {} # set to new dict every ep

        self.d_ai = {
                "last reward":      0,
                "total reward":     0,
                "avg loss":         float(0),
                "epsilon":          0,
                }

        self.d_game = {
                "points":           0,
                "turns":            0,
                "board fill ratio": 0,
                }

        self.d_average = {
                "turns":            float(0),
                "final reward":     float(0),
                "game points":      float(0),
                "loss":             float(0),
                }

        self.d_highscores = {
                "turns":            (0,0),
                "final reward":     (0,0),
                "game points":      (0,0),
                }

        self.d_misc = {
                "total turns":      0,
                "episode count":    0,
                "total episodes":   total_episode_count,
                }

        # for looping through these
        self._ds = {
                "AI":         self.d_ai,
                "Game":       self.d_game,
                "Averages":   self.d_average,
                "Highscores": self.d_highscores,
                "Misc":       self.d_misc,
                "RewardList": self.d_reward_list,
                }

    # +------------------------------------------------+
    # |                      API                       |
    # +------------------------------------------------+
    def update(self, data: dict):
        t = data.get("type")
        if not (t and t in ["episode", "session"]):
            raise ValueError("Missing or invalid type for stats")

        if t == "episode":
            self._update_episode(data)
        else: # must be session
            self._update_session(data)


    def new_episode(self):
        ai = self.d_ai
        game = self.d_game
        misc = self.d_misc

        # ── log relevant data ─────────────────────────────────────────────
        log_data = {
                "final reward": self.d_ai["total reward"],
                "avg loss":     self.d_ai["avg loss"],
                "game points":  self.d_game["points"],
                "turns":        self.d_game["turns"],
                }
        self._data_log.append(log_data)

        # ── update averages + highscore ───────────────────────────────────────
        self.__update_averages()
        self.__update_highscores()

        # ── reset values ──────────────────────────────────────────────────────
        # incrementing
        misc["episode count"]    += 1

        ai["last reward"]         = 0
        ai["total reward"]        = 0
        ai["avg loss"]            = 0
        game["points"]            = 0
        game["turns"]             = 0
        game["board fill ratio"]  = 0
        self._loss_log            = []

    def get_str(self):
        final_str = []       

        def gen_title(s):
            return f"-- {s} ---------"
        
        def d_to_s(d):
            s = [f"{key:35}: {d[key]}" for key in d]
            return '\n'.join(s)

        def stack(list, nSections):
            titles = [n for n in range(nSections) if n%2 == 0]
            bodies = [n for n in range(nSections) if n%2 == 1]


        self.__round_floats() # working with floats T_T

        for k,v in self._ds.items():
            final_str.append(gen_title(k))
            final_str.append(d_to_s(v))

        return '\n'.join(final_str)

    def get_save_data(self):
        d = {
                "Averages": self.d_average,
                "Highscores": self.d_highscores
                }
        return d

    def load_save_data(self, data):
        pass



    # +------------------------------------------------+
    # |                 Update Helpers                 |
    # +------------------------------------------------+
    def _update_episode(self, data):
        ai = self.d_ai
        game = self.d_game
        misc = self.d_misc
        rl = self.d_reward_list

        """
        - last reward
        - loss
        - game points
        - board fill
        """
        # game
        game["board fill ratio"]  = data["board_fill_ratio"]
        game["points"]           += data["points"]
        game["turns"]            += 1
        misc["total turns"]      += 1

        # ai
        ai["last reward"]         = data["reward"]
        ai["total reward"]       += data["reward"]

        # reward list
        rl.update(data["reward_list"])

        # loss
        self._loss_log.append(data["loss"])
        ai["avg loss"] = sum(self._loss_log) / len(self._loss_log)


    def _update_session(self, data):
        ai   = self.d_ai
        game = self.d_game
        avgs = self.d_average
        high = self.d_highscores
        misc = self.d_misc

        """
        - epsilon
        """

        # value setting
        ai["epsilon"] = data["epsilon"]


    # +------------------------------------------------+
    # |              Averages / Highscore              |
    # +------------------------------------------------+
    def __update_averages(self):
        ai   = self.d_ai
        game = self.d_game
        misc = self.d_misc
        avgs = self.d_average
        log  = self._data_log

        def get_avg(feat):
            avg = sum(d[feat] for d in self._data_log) / len(self._data_log)
            return round(avg, DECIMAL_CUTOFF)

        # Steps
        avgs["turns"] = get_avg("turns")
        # Final reward
        avgs["final reward"] = get_avg("final reward")
        # Game points
        avgs["game points"] = get_avg("game points")
        # Loss
        avgs["loss"] = get_avg("avg loss")

    def __update_highscores(self):
        ai   = self.d_ai
        game = self.d_game
        high = self.d_highscores
        misc = self.d_misc

        # format: (value, episode number)
        # Steps
        if game["turns"] > high["turns"][0]:
            high["turns"] = (game["turns"], misc["episode count"])

        # Final reward
        if ai["total reward"] > high["final reward"][0]:
            high["final reward"] = (ai["total reward"], misc["episode count"])

        # In-game Points
        if game["points"] > high["game points"][0]:
            high["game points"] = (game["points"], misc["episode count"])

    def __round_floats(self):
        def round_floats(d):
            for key in d:
                if isinstance(d[key], float):
                    d[key] = round(d[key], 2)

        for d in self._ds.values():
            round_floats(d)


        

    

