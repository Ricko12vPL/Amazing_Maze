# maze_toolkit.py
# Minimalny, czytelny toolkit do pracy z perfect mazes
import random
from collections import deque, namedtuple
import math

# Reprezentacja:
# - komórki (cell) indexowane (r,c) w komórkowej siatce w x h
# - grid_chars: 2*h+1 x 2*w+1, 1=wall,0=passage (łatwe do ASCII/SVG)

Cell = namedtuple("Cell", ["r","c"])

class Maze:
    def __init__(self, width, height, mask=None):
        """
        width, height = liczba komórek (szer x wys)
        mask: opcjonalna funkcja is_allowed(r,c) lub set of allowed Cell
        """
        self.w = width
        self.h = height
        self.mask = None
        if mask is not None:
            if callable(mask):
                self.mask = mask
            else:
                allowed = set(mask)
                self.mask = lambda r,c: Cell(r,c) in allowed
        # initialize grid of walls (2*h+1 x 2*w+1)
        self.grid_h = 2*self.h + 1
        self.grid_w = 2*self.w + 1
        self.grid = [[1 for _ in range(self.grid_w)] for _ in range(self.grid_h)]
        # set cell centers as passages only if allowed
        for r in range(self.h):
            for c in range(self.w):
                if (self.mask is None) or self.mask(r,c):
                    self.grid[r*2+1][c*2+1] = 0
        # internal: easy cell list
        self.cells = [(r,c) for r in range(self.h) for c in range(self.w) if (self.mask is None or self.mask(r,c))]

    def in_bounds_cell(self, r,c):
        return 0 <= r < self.h and 0 <= c < self.w and (self.mask is None or self.mask(r,c))

    def cell_to_grid(self, r,c):
        return (r*2+1, c*2+1)

    def remove_wall_between(self, a, b):
        # a,b are (r,c) cells adjacent
        ar,ac = a; br,bc = b
        gr = (ar+br) + 1
        gc = (ac+bc) + 1
        # since grid cell coords = 2*cell+1, wall coords = ar*2+1 + (br-ar)
        self.grid[ar+br+1][ac+bc+1] = 0
        # but above formula is wrong as integers; use proper:
        ga_r, ga_c = self.cell_to_grid(ar,ac)
        gb_r, gb_c = self.cell_to_grid(br,bc)
        wall_r = (ga_r + gb_r)//2
        wall_c = (ga_c + gb_c)//2
        self.grid[wall_r][wall_c] = 0

    def ascii(self):
        return "\n".join("".join("█" if val else " " for val in row) for row in self.grid)

    # ---- GENERATORS ----
    def generate_recursive_backtracker(self, seed=None, strategy="last"):
        """
        strategy: 'last' (stack, DFS), 'random' (Prim-like), 'first' (queue-like), or probability mix: float p -> pick last with prob p else pick random
        """
        if seed is not None:
            random.seed(seed)
        visited = set()
        cells = [c for c in self.cells]
        if not cells:
            return
        start = random.choice(cells)
        stack = [start]
        visited.add(start)

        while stack:
            # choose index according to strategy
            if isinstance(strategy, float):
                if random.random() < strategy:
                    idx = len(stack)-1
                else:
                    idx = random.randrange(len(stack))
            elif strategy == "last":
                idx = len(stack)-1
            elif strategy == "random":
                idx = random.randrange(len(stack))
            elif strategy == "first":
                idx = 0
            else:
                idx = len(stack)-1
            cell = stack[idx]
            r,c = cell
            neighbors = []
            for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr, nc = r+dr, c+dc
                if self.in_bounds_cell(nr,nc) and (nr,nc) not in visited:
                    neighbors.append((nr,nc))
            if neighbors:
                nb = random.choice(neighbors)
                self.remove_wall_between((r,c), nb)
                visited.add(nb)
                stack.append(nb)
            else:
                stack.pop(idx)

    def generate_kruskal(self, seed=None):
        if seed is not None:
            random.seed(seed)
        # build edges between adjacent allowed cells
        edges = []
        for r,c in self.cells:
            for dr,dc in [(0,1),(1,0)]:  # only right and down to avoid duplicates
                nr, nc = r+dr, c+dc
                if self.in_bounds_cell(nr,nc):
                    edges.append(((r,c),(nr,nc)))
        random.shuffle(edges)
        # union-find
        parent = {}
        def find(u):
            if parent[u] != u:
                parent[u] = find(parent[u])
            return parent[u]
        def union(a,b):
            ra, rb = find(a), find(b)
            if ra==rb: return False
            parent[rb] = ra
            return True
        # init parents
        for c in self.cells:
            parent[c] = c
        for a,b in edges:
            if union(a,b):
                self.remove_wall_between(a,b)

    # ---- SOLVERS ----
    def bfs_solve(self, start_grid, goal_grid):
        """
        start_grid, goal_grid: coordinates on grid (r,c) in grid space (not cell coords)
        return path as list of grid coords
        """
        H, W = self.grid_h, self.grid_w
        q = deque([start_grid])
        parent = {start_grid: None}
        while q:
            cur = q.popleft()
            if cur == goal_grid:
                path = []
                while cur is not None:
                    path.append(cur)
                    cur = parent[cur]
                path.reverse()
                return path
            r,c = cur
            for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                nr, nc = r+dr, c+dc
                if 0 <= nr < H and 0 <= nc < W and self.grid[nr][nc] == 0 and (nr,nc) not in parent:
                    parent[(nr,nc)] = cur
                    q.append((nr,nc))
        return None

# ---------- Example usage ----------
if __name__ == "__main__":
    # generujemy przykłady
    m = Maze(20,12)
    m.generate_recursive_backtracker(seed=42, strategy="last")
    # otwory wejścia/wyjścia
    m.grid[0][1] = 0
    m.grid[m.grid_h-1][m.grid_w-2] = 0
    print(m.ascii())

    # solve
    start = (0,1)
    goal = (m.grid_h-1, m.grid_w-2)
    path = m.bfs_solve(start, goal)
    if path:
        # zaznacz ścieżkę kropkami dla display; zrobimy kopię
        display = [row[:] for row in m.grid]
        for (r,c) in path:
            if display[r][c] == 0:
                display[r][c] = 2
        # print ascii with marks
        symbols = {1:"█", 0:" ", 2:"."}
        print("\nTrasa:")
        for row in display:
            print("".join(symbols.get(x," ") for x in row))
    else:
        print("Brak ścieżki (coś nie tak).")
