# Jump Point Search Algorithm
import heapq

def pathfind(grid, start, goal):
    def heuristic(a, b):
        dx = abs(a[0] - b[0])
        dy = abs(a[1] - b[1])
        return dx + dy

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

    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current_f, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1], g_score[goal]

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            nx, ny = current[0] + dx, current[1] + dy
            if not (0 <= nx < len(grid)) or not (0 <= ny < len(grid[0])) or grid[nx][ny] == 1:
                continue

            jump_point = jump(nx, ny, current[0], current[1])
            if jump_point:
                jx, jy = jump_point
                tentative_g = g_score[current] + abs(jx - current[0]) + abs(jy - current[1])

                if jx == goal[0] and jy == goal[1]:
                    tentative_g = g_score[current] + abs(goal[0] - current[0]) + abs(goal[1] - current[1])

                if (jx, jy) not in g_score or tentative_g < g_score[(jx, jy)]:
                    came_from[(jx, jy)] = current
                    g_score[(jx, jy)] = tentative_g
                    f_score[(jx, jy)] = tentative_g + heuristic((jx, jy), goal)
                    heapq.heappush(open_set, (f_score[(jx, jy)], (jx, jy)))

    return [], None