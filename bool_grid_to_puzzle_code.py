from load_bool_grid import load_boolean_grid


def count_adjacent_zeros(grid, row, col):
    count = 0
    height = len(grid)
    width = len(grid[0])
    
    # Check all 9 adjacent cells
    for i in range(-1, 2):
        for j in range(-1, 2):
            # Check if adjacent cell is within grid bounds
            adj_row = row + i
            adj_col = col + j
            if 0 <= adj_row < height and 0 <= adj_col < width:
                # Count if adjacent cell is False (0)
                if not grid[adj_row][adj_col]:
                    count += 1
    
    return count

def bool_grid_to_counts(bool_grid):
    if not bool_grid or not bool_grid[0]:
        return []
        
    height = len(bool_grid)
    width = len(bool_grid[0])
    
    count_grid = []
    for row in range(height):
        count_row = []
        for col in range(width):
            count_row.append(count_adjacent_zeros(bool_grid, row, col))
        count_grid.append(count_row)
        
    return count_grid

def save_grid_to_file(grid, file_path):
    output_str = ''
    for row in grid:
        row_str = ''.join(map(str, row)) + '\n'
        output_str += row_str
    print(output_str)
    with open(file_path, 'w') as file:
        file.write(output_str)

    

if __name__ == "__main__":
    bool_grid = load_boolean_grid('bool_grid.txt')
    count_grid = bool_grid_to_counts(bool_grid)
    save_grid_to_file(count_grid, 'count_grid.txt')
