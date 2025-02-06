# Example:
# 453
# 453
# 221
# to
# 4--
# -5-
# -2-
# Encode as a SAT problem using Sequential Counter encoding (de Jong 2023 p.19)
# each grid bool is a variable, e.g. grid[2,3] > c23
# each number clue is a maximum-true constraint,
#   e.g. 3 at grid[2,3] is (max_3(c12, c13, c14, c22, c23, c24, c32, c33, c34) AND
#       max_6(~c12, ~c13, ~c14, ~c22, ~c23, ~c24, ~c32, ~c33, ~c34))
