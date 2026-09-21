from collections import deque

def printBoard(board_arr):
    n_rows, n_cols = 10, 10

    for _ in range(n_cols + 2):     # +2 -> plus 1 for each "wall" on each side
        print("-", end = '   ')
    print()

    for row in board_arr:
        print("|", end = '   ')
        for unit in row:
            print("X" if unit else ' ', end = '   ')
        print("|")

    for _ in range(n_cols + 2):
        print("-", end = '   ')
    print()

    return 

def reward_test1(board_arr):
    def longest_continuous_blocks(line):
        max_c = 0
        c = 0
        for x in range(len(line)):
            if line[x]:
                c += 1
            else:
                max_c = max(max_c, c)
                c = 0
        print(f"max_c: {max_c}")
        return max_c

    def get_board_cols():
        cols = []
        for cCol in range(len(board_arr)):
            col = [row[cCol] for row in board_arr]
            cols.append(col)
        return cols

    value = 0

    value += sum([longest_continuous_blocks(row) for row in board_arr])
    value += sum([longest_continuous_blocks(col) for col in get_board_cols()])

    return value

def reward_test2(board_arr):
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
                value -= 3
            else:
                value -= 1

        return value



board_arr = [[0, 1, 0, 0, 0, 0, 0, 0, 0, 0], 
             [0, 1, 0, 0, 1, 1, 1, 1, 0, 0], 
             [1, 1, 1, 0, 1, 0, 0, 1, 0, 0], 
             [0, 1, 0, 0, 1, 0, 0, 1, 0, 0],
             [0, 1, 0, 0, 1, 1, 1, 1, 0, 1],
             [1, 1, 1, 1, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 1, 0, 0, 0, 0, 0, 1],
             [1, 0, 0, 1, 1, 0, 0, 0, 0, 0],
             [1, 0, 0, 1, 0, 1, 0, 0, 0, 0],
             [1, 0, 0, 1, 1, 0, 0, 0, 0, 0]]




