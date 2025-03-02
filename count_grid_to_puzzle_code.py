from typing import List
import file_io
import sys
from process_count_grid import encode_grid_as_tatham_string

# Format in:
# 4--
# -5-
# -2-

# Format out:
# '#3x3:4c5b2a'
if __name__ == "__main__":
    input_file = 'count_grid.txt'
    output_file = 'tatham_encoding.txt'

    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]

    count_grid: List[str] = file_io.load_count_grid(input_file)
    tatham_string: str = encode_grid_as_tatham_string(count_grid)
    with open(output_file, 'w') as f:
        f.write(tatham_string)
    print(tatham_string)