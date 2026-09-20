from torch._C import Value
from Game.Board.Board import Board
from Game.Shape.Shape import Shape
from collections      import deque

NUM_BLOCKS_CLOSE_TO_FILLING = 6

class RewardCalculator:
    def __init__(self, board: "Board", discount=0.99):
        self._board          = board
        self._discount       = discount

        self._data = {
                "last_move": (),
                "can_play": False,
                }

        self._reward_info = {}

        self._print_rewards = False

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


    def calc(self):
        d = self._data

        death_penalty = -200
        fr = self._board.utils.get_filled_ratio()

        rewards = {
                "fill_penalty": 0.5 * -( (10*fr)**2 ),
                "line_prog_reward":  0.1 * self._line_progress_reward(),
                # "connects_blocks": 0.1 * self._connects_blocks_reward(),
                "line_clear_reward": self._line_clear_reward(),
                "shaping_reward":    self._get_shaping_reward(discount=self._discount),
                }

        self._reward_info.update(rewards)

        return sum(rewards[k] for k in rewards) if self._data["can_play"] else death_penalty, self._reward_info

    def enable_print_rewards(self):
        self._print_rewards = True


    # +------------------------------------------------+
    # |              Reward Calculations               |
    # +------------------------------------------------+
    def _line_progress_reward(self):
        """
        rewards 
        """

        info = {}

        def connected_blocks(line, placed_inds):
            """
            returns number of blocks connected to the placed
            section
            """
            p = sorted(placed_inds)
            c = 0

            l = p[0]
            r = p[-1]

            while r+1 < len(line) and line[r+1]:
                c += 1
                r += 1

            while 0 <= l-1 and line[l-1]:
                c += 1
                l -= 1

            return c

        def count_blocks(line):
            return sum([1 if x else 0 for x in line])

        rRwd   = 0 # row reward
        cRwd   = 0 # col reward
        bP    = self._data["placed_block_positions"]
        uRows = set([x[0] for x in bP])
        uCols = set([x[1] for x in bP])

        for u in uRows:
            placed_inds = [x[1] for x in bP if x[0] == u]
            board_row = self._board.get_row(u)
            nb = count_blocks(board_row) - len(placed_inds)
            cb = connected_blocks(board_row, placed_inds)

            rRwd += ( cb * 2 ) + ( nb - cb )

        for u in uCols:
            placed_inds = [x[0] for x in bP if x[1] == u]
            board_col = self._board.get_col(u)
            nb = count_blocks(board_col) - len(placed_inds)
            cb = connected_blocks(board_col, placed_inds)

            cRwd += ( cb * 2 ) + ( nb-cb )

        self._reward_info.update({
            "(line pg) rows": rRwd,
            "(line pg) cols": cRwd,
            })

        return rRwd + cRwd

    def _connects_blocks_reward(self):
        """
        rewards agent for placing a piece that fills a hole in a row/col
        """
        def connect_check(line, placed_on_line):

            # get left-most and right-most block
            p = sorted(placed_on_line)
            l = p[0]
            r = p[-1]

            # check if there is an empty cell next to them
            # not line-1 or 
            if 0 <= l-1 and not line[l-1]:
                return False
            if r+1 < len(line) and not line[r+1]:
                return False

            return True
        
        rRwd = 0
        cRwd = 0

        bP = self._data["placed_block_positions"]

        uRows = set([x[0] for x in bP])
        uCols = set([x[1] for x in bP])

        for u in uRows:
            placed_on_line = [x[1] for x in bP if x[0] == u]
            rRwd += 10 if connect_check(self._board.get_row(u), placed_on_line) else 0

        for u in uCols:
            placed_on_line = [x[0] for x in bP if x[1] == u]
            cRwd += 10 if connect_check(self._board.get_col(u), placed_on_line) else 0

        self._reward_info.update({
            "(connect reward) row": rRwd,
            "(connect reward) col": cRwd,
            })

        return rRwd + cRwd


    
    def _line_clear_reward(self):
        reward = 0

        # inverse board fill ratio
        ibfr = 1 - self._board.utils.get_filled_ratio()

        if self._board.get_point_diff():
            reward += 100
            reward += 100 * ibfr


        return reward




    # +------------------------------------------------+
    # |                 Shaping Reward                 |
    # +------------------------------------------------+
    def _get_shaping_reward(self, discount=0.99):
        def board_state_eval(board_arr):
            val1 = self.__board_value_line_completion(board_arr)
            val2 = self.__board_value_holes(board_arr)
            return val1 + val2

        curr_board = self._board.get_board()
        prev_board = self._board.get_prev_board()

        return discount * board_state_eval(curr_board) - board_state_eval(prev_board)


    # +------------------------------------------------+
    # |             Shaping reward helpers             |
    # +------------------------------------------------+
    def __board_value_line_completion(self, board_arr):
        """
        reward based on longest continuous row and longest continuous col
        """

        # ── helper fncs ───────────────────────────────────────────────────────
        def get_board_cols():
            """
            returns all columns in board_arr param
            """
            cols = []
            for cCol in range(len(board_arr)):
                col = [row[cCol] for row in board_arr]
                cols.append(col)
            return cols

        def longest_continuous_blocks(line):
            """
            takes an array and counts longest consecutive 1s
            """
            max_c = 0
            c = 0
            for x in range(len(line)):
                if line[x]:
                    c += 1
                else:
                    c = 0
                max_c = max(max_c, c)
            return max_c

        def calc_line_value(line):
            """
            takes an array and calculates its value
            value:
                -> empty is worth a full line
            """
            v = 0

            nBlks = sum(1 if x else 0 for x in line)

            if nBlks == 0:
                v += 10
            elif nBlks >= 3:
                v += nBlks

            return v

        # ──────────────────────────────────────────────────────────────────────

        vR = 0 # val row
        vC = 0 # val col

        for row in board_arr:
            vR += calc_line_value(row)
        for col in get_board_cols():
            vC += calc_line_value(col)

        self._reward_info.update({
            "(SR.line_val) row": vR,
            "(SR.line_val) col": vC,
            })

        return vR + vC

    def __board_value_holes(self, board_arr):
        """
        Reduce value based on how many cells are in a hole
        (surrounded by blocks)
        """
        value = 0

        rows, cols = len(board_arr), len(board_arr[0])
        visited = [[False]*cols for _ in range(rows)]

        def solo_check(hole):
            # checks if a hole is by itself
            sr,sc = hole
            for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                if not board_arr[sr+dr][sc+dc]:
                    return False
            return True


        def bfs(sr, sc):
            q = deque([(sr, sc)])
            visited[sr][sc] = True
            while q:
                r, c = q.popleft()
                for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
                    nr, nc = r+dr, c+dc
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if not board_arr[nr][nc] and not visited[nr][nc]:
                            visited[nr][nc] = True
                            q.append((nr, nc))

        # 1. Flood fill from every False cell on the border
        for r in range(rows):
            for c in (0, cols-1):
                if not board_arr[r][c] and not visited[r][c]:
                    bfs(r, c)
        for c in range(cols):
            for r in (0, rows-1):
                if not board_arr[r][c] and not visited[r][c]:
                    bfs(r, c)

        # 2. Any unvisited False cell is part of a hole
        holes = [(r, c) for r in range(rows) for c in range(cols)
                 if not board_arr[r][c] and not visited[r][c]]

        nHoles     = 0
        punishment = -100 # 1/19 chance to get single block to fix it, 3/19 a turn

        for hole in holes:
            nHoles += 1 if solo_check(hole) else 0

        self._reward_info.update({"(SR.holes) count": nHoles})

        return nHoles * punishment

