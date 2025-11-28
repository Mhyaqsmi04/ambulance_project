from collections import namedtuple

Cell = namedtuple("Cell", ["type", "value"])


class GridMap:
    def __init__(self, rows, cols, grid):
        self.rows = rows
        self.cols = cols
        self.grid = grid

        self.starts = []
        self.goals = []

        for r in range(rows):
            for c in range(cols):
                cell = grid[r][c]
                if cell.type == "S":
                    self.starts.append((r, c))
                elif cell.type == "G":
                    self.goals.append((r, c))

    @staticmethod
    def parse_from_lines(lines):
        header = lines[0].strip().split()
        if len(header) == 2 and header[0].isdigit():
            rows = int(header[0])
            cols = int(header[1])
            data_lines = lines[1:1+rows]
        else:
            data_lines = lines
            rows = len(data_lines)
            cols = len(data_lines[0])

        grid = []
        for r in range(rows):
            row = []
            for ch in data_lines[r].strip():
                if ch == "S":
                    row.append(Cell("S", 1))
                elif ch == "G":
                    row.append(Cell("G", 1))
                elif ch == "L":
                    row.append(Cell("L", None))
                elif ch.isdigit():
                    row.append(Cell("N", int(ch)))
                else:
                    raise Exception("Invalid map char:", ch)
            grid.append(row)

        return GridMap(rows, cols, grid)

    def in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def cell(self, r, c):
        return self.grid[r][c]

    def neighbors(self, r, c):
        dirs = [
            (-1, 0, "UP"),
            (1, 0, "DOWN"),
            (0, -1, "LEFT"),
            (0, 1, "RIGHT"),
        ]
        for dr, dc, act in dirs:
            nr, nc = r + dr, c + dc
            if self.in_bounds(nr, nc):
                yield nr, nc, act

        yield r, c, "STAY"
