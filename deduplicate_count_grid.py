# Example:
# 453
# 453
# 221
# to
# 4--
# -5-
# -2-

# Format in:
# 4--
# -5-
# -2-
# Format out:
# (4, [1,2,4,5]),
# (5, [1,2,3,4,5,6,7,8,9]),
# (2, [4,5,6,7,8,9])

from puzzle_simplifier import simplify_puzzle

def load_count_grid(filename):
    grid = []
    with open(filename) as f:
        for line in f:
            row = []
            for c in line.strip():
                if c == '-':
                    row.append(c)
                else:
                    row.append(int(c))
            grid.append(row)
    return grid

if __name__ == "__main__":
    existing_puzzle = load_count_grid('count_grid.txt')
    simplified = simplify_puzzle(existing_puzzle)