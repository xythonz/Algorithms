#jumpPoint.py
import heapq

def jump_point(grid, start, goal, heuristic):
    def jump(x, y, px, py):
        if not (0 <= x < len(grid)) or not (0 <= y < len(grid[0])) or grid[x][y] == 1:
            return None
        if (x, y) == goal:
            return (x, y)

        dx = x - px
        dy = y - py

        if dx != 0 and dy != 0:
            if (jump(x + dx, y, x, y) is not None or
                jump(x, y + dy, x, y) is not None):
                return (x, y)
            if (grid[x - dx][y + dy] == 0 and grid[x - dx][y] == 1) or \
               (grid[x + dx][y - dy] == 0 and grid[x][y - dy] == 1):
                return (x, y)
        else:
            if dx != 0:
                if (grid[x + dx][y + 1] == 0 and grid[x][y + 1] == 1) or (grid[x + dx][y - 1] == 0 and grid[x][y - 1] == 1):
                      return (x, y)
            else:
                if (grid[x + 1][y + dy] == 0 and grid[x + 1][y] == 1) or (grid[x - 1][y + dy] == 0 and grid[x - 1][y] == 1):
                        return (x, y)
        if dx != 0 and dy != 0:
            return jump(x + dx, y + dy, x, y)
        else:
            if dx != 0:
                return jump(x + dx, y, x, y)
            else:
                return jump(x, y + dy, x, y)