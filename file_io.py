from typing import List, Optional, Tuple, Dict
import json

def save_boolean_grid(grid: List[List[int]], file_path: str) -> None:
    output_str = ''
    for row in grid:
        row_str = ''.join(str(int(x)) if (x is not None and x >= 0) else '-' for x in row) + '\n'
        output_str += row_str
    print(output_str)
    with open(file_path, 'w') as file:
        file.write(output_str)

def save_count_grid(grid: List[List[int]], file_path: str) -> None:
    output_str = ''
    for row in grid:
        row_str = ''.join(str(x) if (x is not None and x >= 0) else '-' for x in row) + '\n'
        output_str += row_str
    print(output_str)
    with open(file_path, 'w') as file:
        file.write(output_str)

def load_boolean_grid(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        bool_grid = []
        for line in lines:
            row = [char == '#' for char in line.strip()]
            bool_grid.append(row)
            
        return bool_grid
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def load_count_grid(filename: str) -> List[List[Optional[int]]]:
    grid: List[List[Optional[int]]] = []
    with open(filename) as f:
        for line in f:
            row: List[Optional[int]] = []
            for c in line.strip():
                if c == '-':
                    row.append(None)
                else:
                    row.append(int(c))
            grid.append(row)
    return grid

def save_constraints(constraints: List[Tuple[int, List[int]]], constraints_file: str) -> None:
    with open(constraints_file, 'w') as f:
        f.write(json.dumps(constraints))

def save_var_mapping(var_mapping: Dict[Tuple[int, int], int], mapping_file: str) -> None:
    serialized_mapping = {f"{x},{y}": v for (x,y), v in var_mapping.items()}
    with open(mapping_file, 'w') as f:
        f.write(json.dumps(serialized_mapping))
