from torch._C import Value
from Game.Board.Board import Board
from Game.Shape.Shape import Shape
from collections      import deque

NUM_BLOCKS_CLOSE_TO_FILLING = 7

class RewardCalculator:
    def __init__(self, board: "Board", discount=0.99):
        self._board          = board
        self._discount       = discount

        self._data = {
                "last_move": (),
                "can_play": False,
                }

        self._print_rewards = False

    # ╭────────────────────────────────────────────────╮
    # │                      API                       │
    # ╰────────────────────────────────────────────────╯
    def update(self, data: dict):
        for key in data:
            if key not in self._data:
                raise RuntimeError(f"Invalid Dict passed to RewardCalculator. Invalid key = {key}")

        self._data.update(data)

    def calc(self):
        d = self._data

        fill_ratio = self._board.utils.get_filled_ratio()

        rewards = {
                # scale by 10 so the power will work as intended then scale back down
                # "fill_penalty": -0.5 * (10 * fill_ratio)**2,
                # think it might be better to ignore multi-lines for training
                "line_clear_reward": self._line_clear_reward(),
                "line_prog_reward": (1-fill_ratio)**2 * ( 0.1 * self._line_progress_reward() ),
                "shaping_reward": self._get_shaping_reward(discount=0.99)
                }

        if self._print_rewards:
            for k in rewards:
                print(f"{k}: {rewards[k]}")

        if self._data["can_play"]:
            return sum(rewards[k] for k in rewards)
        else:
            return -300

    def enable_print_rewards(self):
        self._print_rewards = True


    # +------------------------------------------------+
    # |              Reward Calculations               |
    # +------------------------------------------------+
    def _line_progress_reward(self):
        """
        rewards building towards a line
        > blocks on the same line count for higher reward
        > connected blocks are rewarded more
        """

        def connected_blocks(line, ind):
            c = 0
            ptr = ind+1
            while ptr < len(line) and line[ptr]:
                c += 1
                ptr += 1

            ptr = ind-1
            while 0 <= ptr and line[ptr]:
                c += 1
                ptr -= 1

            return c
        
        def blocks_on_line(line):
            return sum([1 if x else 0 for x in line])


        reward         = 0
        max_row_reward = 0
        max_col_reward = 0

        b               = self._board
        shape,pos       = self._data["last_move"]
        block_positions = self._board.utils.get_shape_block_positions(shape, pos)

        rows            = [x[0] for x in block_positions]
        cols            = [x[1] for x in block_positions]

        for c_row in set(rows):
            # choose a random block on the row
            piece_on_row = next(bPos for bPos in block_positions if bPos[0] == c_row)

            cReward = 0
            r       = self._board.get_row(piece_on_row[0])
            nBlk    = blocks_on_line(r)

            cReward += connected_blocks(r, piece_on_row[1])
            if (nBlk >= NUM_BLOCKS_CLOSE_TO_FILLING):
                cReward += nBlk

            max_row_reward = max(max_row_reward, cReward)

            
        for c_col in set(cols):
            piece_on_col = next(bPos for bPos in block_positions if bPos[1] == c_col) # list of positions w/ this col

            cReward = 0
            c       = self._board.get_col(piece_on_col[1])
            nBlk = blocks_on_line(c)

            cReward += connected_blocks(c, piece_on_col[0])
            max_col_reward = max(max_col_reward, cReward)

            if (nBlk >= NUM_BLOCKS_CLOSE_TO_FILLING):
                reward += nBlk

        if self._print_rewards:
            print(f"max row reward: {max_row_reward}")
            print(f"max col reward: {max_col_reward}")

        reward += max_row_reward ** 2
        reward += max_col_reward ** 2

        return reward
    
    def _line_clear_reward(self):
        reward = 0

        if self._board.get_point_diff():
            reward += 100
            reward += 100 * (1 - self._board.utils.get_filled_ratio())

        return reward




    # +------------------------------------------------+
    # |                 Shaping Reward                 |
    # +------------------------------------------------+
    def _get_shaping_reward(self, discount=0.99):
        def eval_board(board_arr):
            val1 = self.__board_value_line_completion(board_arr)
            val2 = self.__board_value_holes(board_arr)

            return val1 + val2

        curr_board = self._board.get_board()
        prev_board = self._board.get_prev_board()

        return discount * eval_board(curr_board) - eval_board(prev_board)


    # +------------------------------------------------+
    # |             Shaping reward helpers             |
    # +------------------------------------------------+
    def __board_value_line_completion(self, board_arr):
        """
        reward based on longest continuous row and longest continuous col
        """
        def longest_continuous_blocks(line):
            max_c = 0
            c = 0
            for x in range(len(line)):
                if line[x]:
                    c += 1
                else:
                    c = 0
                max_c = max(max_c, c)
            return max_c

        def get_board_cols():
            cols = []
            for cCol in range(len(board_arr)):
                col = [row[cCol] for row in board_arr]
                cols.append(col)
            return cols

        value = 0
        max_row_reward = 0
        max_col_reward = 0

        for row in board_arr:
            max_row_reward = max(max_row_reward, longest_continuous_blocks(row))
        for col in get_board_cols():
            max_col_reward = max(max_col_reward, longest_continuous_blocks(col))

        value += max_row_reward + max_col_reward

        return value

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

        for hole in holes:
            if solo_check(hole):
                value -= 100

        return value


    # ╭────────────────────────────────────────────────╮
    # │              Calculator Functions              │
    # ╰────────────────────────────────────────────────╯
    # def _adjacent_blocks_reward(self):
    #     if self._last_move is None:
    #         raise RuntimeError("Cannot calculate reward without knowing last move")
    #
    #     reward                = 0
    #     shape, pos, block_pos = self._last_move
    #     b                     = self._board
    #
    #     # +------------------------------------------------+
    #     # | search in a cross around each block. exclude   |
    #     # | blocks that are within the placed shape.       |
    #     # +------------------------------------------------+
    #     for block in block_pos:
    #         r,c = block # (row,col) 
    #
    #         for t_row in [r+1, r-1]: # target row
    #             target = (t_row, c)
    #             if b.utils.is_valid_pos(target) and b.get(target) and (target not in block_pos):
    #                 reward += 1
    #
    #         for t_col in [c+1,c-1]:
    #             target = (r, t_col)
    #             if b.utils.is_valid_pos(target) and b.get(target) and (target not in block_pos):
    #                 reward += 1
    #
    #     return reward
