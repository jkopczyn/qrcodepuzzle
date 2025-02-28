from typing import List

def encode_grid_as_tatham_string(grid: List[str]) -> str:
    if not grid or not grid[0]:
        return "#0x0:"
    height: int = len(grid)
    width: int = len(grid)
    if height != width:
        raise ValueError("Grid must be square")
    puzzle_string: str = f"#{height}x{width}:"
    current_blanks: int = 0

    # Flatten grid into sequence and convert strings to integers
    flattened: List[int] = []
    for row in grid:
        for cell in row:
            if cell == '-':
                flattened.append(-1)
            else:
                flattened.append(int(cell))

    for num in flattened:
        if num < 0:
            current_blanks += 1
            if current_blanks == 26:
                puzzle_string += 'z'
                current_blanks = 0
        else:
            if current_blanks > 0:
                puzzle_string += chr(ord('a') + current_blanks - 1)
                current_blanks = 0
            puzzle_string += str(num)

    if current_blanks > 0:
        puzzle_string += chr(ord('a') + current_blanks - 1)    
    return puzzle_string

if __name__ == "__main__":
    with open('count_grid.txt', 'r') as f:
        count_grid: List[str] = f.read().splitlines()
    tatham_string: str = encode_grid_as_tatham_string(count_grid)
    with open('tatham_encoding.txt', 'w') as f:
        f.write(tatham_string)
    print(tatham_string)