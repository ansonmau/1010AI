import subprocess
from Game.Board.Board import Board
from Game.Shape.Shape import Shape
from collections      import deque

NUM_BLOCKS_CLOSE_TO_FILLING = 6

class RewardCalculator:
    def __init__(self, board: "Board", discount=0.99):
        self._board                = board
        self._discount             = discount

        self._prev = {
                "board_value": float(0),
                }

        self._data = {
                "last_move": (),
                "can_play": False,
                }

        self._reward_info = {}

    # ╭────────────────────────────────────────────────╮
    # │                      API                       │
    # ╰────────────────────────────────────────────────╯
    def update(self, data: dict):
        for key in data:
            if key not in self._data:
                raise RuntimeError(f"Invalid Dict passed to RewardCalculator. Invalid key = {key}")

        self._data.update(data)
        self._data.update({
            "placed_block_positions": self._board.utils.get_shape_block_positions(*self._data["last_move"]),
            })

    def new_episode(self):
        self._prev["board_value"] = self.__BV_eval(self._board.get_board())


    def calc(self):
        d = self._data

        death_penalty = -500
        fr = self._board.utils.get_filled_ratio()

        rewards = {
                "[ Final ] avail moves penalty": 0.05 * self._penalty_availMoves(),
                "[ Final ] hole penalty":        0.1 * self._penalty_holes(),
                "[ Final ] line clear reward":   self._reward_lineClear(),
                "[ Final ] shaping reward":      0.1 * self._get_shaping_reward(discount=self._discount),
                }

        self._reward_info.update(rewards)

        return sum(rewards[k] for k in rewards) if self._data["can_play"] else death_penalty, self._reward_info


    # +------------------------------------------------+
    # |              Reward calculations               |
    # +------------------------------------------------+
    def _reward_lineClear(self):
        reward = 0

        # inverse board fill ratio
        ibfr = 1 - self._board.utils.get_filled_ratio()

        if self._board.get_point_diff():
            reward += 100
            reward += 100 * ibfr

        return reward
    
    def _penalty_holes(self):
        cb = self._board.get_board()

        return self.__scan_numHoles(cb)

    def _penalty_availMoves(self):
        def close(n, M):
            """
            returns closest increment of M
            """

            m = M//2
            r = n%M
            b = n//M

            if r <= m:
                return M * b
            else:
                return M * (b+1)


        final_penalty = 0
        t = 400
        nL = self.__scan_numLegalMoves(self._board.get_board())
        if nL < t:
            final_penalty = close(t-nL, 100)

        return -1 * final_penalty

    # +------------------------------------------------+
    # |                 Shaping Reward                 |
    # +------------------------------------------------+
    def _get_shaping_reward(self, discount=0.99):
        cb = self._board.get_board()

        cbV = self.__BV_eval(cb)
        pbV = self._prev["board_value"]

        self._prev.update({
            "board_value": cbV
            })

        self._reward_info.update({
            "[ SR.board_eval ] curr eval": cbV,
            "[ SR.board_eval ] prev eval": pbV,
            })

        return discount * cbV - pbV

    # ── Helpers ───────────────────────────────────────────────────────────
    def __BV_eval(self, board_arr):
        evals = [
                self.__BV_line_progress(board_arr),
                ]
        return sum(evals)


    def __BV_line_progress(self, board_arr):
        """
        reward based on longest continuous row and longest continuous col
        """
        def get_cols(b):
            """
            returns all columns in board_arr param
            """
            cols = []
            for cCol in range(len(b)):
                cols.append([r[cCol] for r in b])
            return cols

        def calc_line_value(line):
            """
            for calculating value of a line
            """
            nBlks = sum(1 if x else 0 for x in line)
            return nBlks ** 2

        vR = 0 # val row
        vC = 0 # val col

        for row in board_arr:
            vR += calc_line_value(row)
        for col in get_cols(board_arr):
            vC += calc_line_value(col)

        self._reward_info.update({
            "[ lineval ] row, col": (vR, vC),
            "[ lineval ] total": vR + vC,
            })

        return vR + vC

    def __scan_numHoles(self, board_arr):
        """
        Find all enclosed empty regions (holes) and penalize based on size.
        Holes >= 9 cells (3x3 equivalent) get no penalty.
        Holes < 9 cells get penalty scaled linearly, maxing out at size 1.
        """
        rows, cols = len(board_arr), len(board_arr[0])
        visited = [[False] * cols for _ in range(rows)]

        def bfs(sr, sc):
            component = [(sr, sc)]
            q = deque([(sr, sc)])
            visited[sr][sc] = True
            while q:
                r, c = q.popleft()
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if not board_arr[nr][nc] and not visited[nr][nc]:
                            visited[nr][nc] = True
                            q.append((nr, nc))
                            component.append((nr, nc))
            return component

        # 1. Flood fill from every False cell on the border (these aren't holes)
        for r in range(rows):
            for c in (0, cols - 1):
                if not board_arr[r][c] and not visited[r][c]:
                    bfs(r, c)
        for c in range(cols):
            for r in (0, rows - 1):
                if not board_arr[r][c] and not visited[r][c]:
                    bfs(r, c)

        # 2. Remaining unvisited False cells form enclosed holes
        FULL_SIZE   = 9    # 3x3 equivalent — holes this size or larger are fine
        MAX_PENALTY = -50  # penalty applied at hole size == 1

        total_penalty = 0
        hole_sizes = []

        for r in range(rows):
            for c in range(cols):
                if not board_arr[r][c] and not visited[r][c]:
                    size = len(bfs(r, c))
                    hole_sizes.append(size)

                    if size < FULL_SIZE:
                        severity = (FULL_SIZE - size) / (FULL_SIZE - 1)
                        total_penalty += MAX_PENALTY * severity

        self._reward_info.update({
            "[ holes ] sizes":         hole_sizes,
            "[ holes ] count":         len(hole_sizes),
            "[ holes ] total penalty": total_penalty,
            })

        return total_penalty

    def __scan_numLegalMoves(self, board_arr, ignore_single=True):
        ignore = [0,1] if ignore_single else []

        all_shapes = Shape.get_all_shapes(ignore=ignore) 
        b = Board.from_arr(board_arr)
        nL = 0 # n legal moves

        for s in all_shapes:
            nL += len(b.check.get_all_valid_positions(s))

        self._reward_info.update({
            "[ legal moves ] count": nL,
            })

        return nL


