from Game.Board.Board import Board
from Game.Shape.Shape import Shape


class RewardCalculator:
    def __init__(self, board: "Board"):
        self._board          = board
        self._agent_can_play = False
        self._last_move      = None

    # ╭────────────────────────────────────────────────╮
    # │                      API                       │
    # ╰────────────────────────────────────────────────╯
    def set_last_move(self, shape: "Shape", pos, agent_can_play):
        self._last_move      = (shape, pos, self._board.utils.get_shape_block_positions(shape,pos))
        self._agent_can_play = agent_can_play

    def calc(self):
        reward = 0

        if not self._agent_can_play:
            reward += self._loss_penalty()
        else:
            # reward += self._line_progress_reward()
            # reward += self._fill_penalty()
            # reward += self._adjacent_blocks_reward()
            reward += self._line_clear_reward()

        return reward


    # ╭────────────────────────────────────────────────╮
    # │              Calculator Functions              │
    # ╰────────────────────────────────────────────────╯

    def _turn_

    def _line_progress_reward2(self):
        if self._last_move is None:
            raise RuntimeError("Cannot calculate reward without knowing last move")
        
        reward                = 0
        shape, pos, block_pos = self._last_move
        b                     = self._board
        
        rows = set([block[0] for block in block_pos])
        cols = set([block[0] for block in block_pos])



    def _adjacent_blocks_reward(self):
        if self._last_move is None:
            raise RuntimeError("Cannot calculate reward without knowing last move")

        reward                = 0
        shape, pos, block_pos = self._last_move
        b                     = self._board

        # +------------------------------------------------+
        # | search in a cross around each block. exclude   |
        # | blocks that are within the placed shape.       |
        # +------------------------------------------------+
        for block in block_pos:
            r,c = block # (row,col) 

            for t_row in [r+1, r-1]: # target row
                target = (t_row, c)
                if b.utils.is_valid_pos(target) and b.get(target) and (target not in block_pos):
                    reward += 1

            for t_col in [c+1,c-1]:
                target = (r, t_col)
                if b.utils.is_valid_pos(target) and b.get(target) and (target not in block_pos):
                    reward += 1

        return reward


    def _fill_penalty(self):
        """
        reduce reward based on how full the board is
        """
        b = self._board

        normalize = 10
        return -normalize * b.utils.get_filled_ratio()
    

    def _line_clear_reward(self):
        """
        give reward based on points gained in game
        """
        return self._board.get_point_diff()

    def _loss_penalty(self):
        """
        penalty for losing
        make sure loss penalty does not drastically outweigh everything else
        """
        penalty = -200

        return 0 if self._agent_can_play else penalty



    def _line_progress_reward(self):
        if self._last_move is None or len(self._last_move) == 0:
            raise RuntimeError("Last move must be set prior to calling this fnc")

        multiplier                = 1
        reward                    = 0

        b                         = self._board
        shape,pos,block_positions = self._last_move
        rows                      = [x[0] for x in block_positions]
        cols                      = [x[1] for x in block_positions]

        for c_row in set(rows):
            col_count = b.get_size()[1] # (n_rows, n_cols)

            # choose a random block on the row
            piece_on_row = next(bPos for bPos in block_positions if bPos[0] == c_row)

            # +1 for every continuous block after it
            col_ptr = piece_on_row[1]
            while col_ptr+1 < col_count and b.get((c_row, col_ptr+1)): 
                if not (c_row, col_ptr+1) in block_positions: # ignore blocks it just placed
                    reward += 1
                col_ptr += 1

            # +1 for every continuous block before it
            col_ptr = piece_on_row[1]
            while 0 <= col_ptr-1 and b.get((c_row, col_ptr-1)): 
                if not (c_row, col_ptr-1) in block_positions: # ignore blocks it just placed
                    reward += 1
                col_ptr -= 1
            
        for c_col in set(cols):
            row_count    = b.get_size()[0]

            # choose a random block
            piece_on_col = next(bPos for bPos in block_positions if bPos[1] == c_col) # list of positions w/ this col

            # +1 for every continuous block below it
            row_ptr      = piece_on_col[0]
            while row_ptr+1 < row_count and b.get((row_ptr+1, c_col)): 
                if not (row_ptr+1, c_col) in block_positions:
                    reward += 1
                row_ptr += 1

            # +1 for every continuous block above it
            row_ptr = piece_on_col[0]
            while 0 <= row_ptr-1 and b.get((row_ptr-1, c_col)): 
                if not (row_ptr-1, c_col) in block_positions:
                    reward += 1
                row_ptr -= 1

        return reward
