import file_io
from process_count_grid import grid_to_constraints
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

if __name__ == "__main__":
    count_grid = file_io.load_count_grid('count_grid.txt')
    constraints, var_mapping = grid_to_constraints(count_grid)
    print(constraints)
    file_io.save_constraints(constraints, 'constraints.txt')
    file_io.save_var_mapping(var_mapping, 'var_mapping.txt')
