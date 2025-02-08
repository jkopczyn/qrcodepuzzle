# Encode as a SAT problem using Sequential Counter encoding (de Jong 2023 p.19)
# each grid bool is a variable, e.g. grid[2,3] > c23
# each number clue is a count-true constraint, expressed as max-true plus a rider
#   e.g. 3 at grid[2,3] is max_3(c12, c13, c14, c22, c23, c24, c32, c33, c34) AND (rider_3)
# max_N/count_N are across M variables x_m, and use M segments of a tracker/counter; these are
#   tracked with new variables s_is, where variable x_1/x1 has variables s_1s for S from 1 to N
#   s21 represents that after including the value of variables x1...x2, 1 variable is true
# example: count_3 on 4 variables [x1, x2, x3, x4]; we have s11, s12, s13, s21, s22, ... s42, s43.
# This is encoded as:
# PROP01  (x1 -> s11) AND        # var1 starts counter if true
# PROP02  (s11 -> x1) AND        # rider: s11 *must* match x1
# PROP03  (x4 -> ~s33) AND       # max_3 constraint itself, if last var is true total must be <3 before it
# PROP04  (~s12 AND ~s13) AND    # impossible to have >1 true in 1 var
# PROP05  (s43) AND              # rider: the last variable must have exactly the right counter
#         (       # iterate for x_i from 1 < i < M
# PROP11  (x2 -> s21) AND  (x2 -> ~s13) AND   # as above, for var x2
# PROP12  (s11 -> s21) AND                    # if counter stands at 1 already it still does
# PROP13  (s21 -> (x2 OR s11)) AND            # rider: and s21 is only true if a prereq is met
#             (       # iterate for s_2j from 1 < j < N
# PROP21      ((x2 AND s11) -> s22) AND (s12 -> s22) AND  # counter stands at 2 if it was 2 or was 1 and +1
# PROP22      (s22 -> (x2 OR s12)) AND (s22 -> (s11 OR s12))  # rider: if and only if
#             ((x2 AND s12) -> s23) AND (s13 -> s23) AND  # continue up to max value of counter
#             (s23 -> (x2 OR s13)) AND (s23 -> (s12 OR s13))  # rider: also continue
#             )       # end iteration for s_2j from 1 < j < N
#         )       # end iteration for x_i from 1 < i < M
#         (x3 -> s31) AND  (x3 -> ~s23) AND
#         (s21 -> s31) AND
#         (s31 -> (x3 OR s21)) AND
#             (       # iterate
#             ((x3 AND s21) -> s32) AND (s22 -> s32) AND
#             (s32 -> (x3 OR s22)) AND (s32 -> (s21 OR s22))
#             ((x3 AND s22) -> s33) AND (s23 -> s33) AND
#             (s33 -> (x3 OR s23)) AND (s33 -> (s22 OR s23))
#             )       # end iteration
#         )       # end iteration
# PROPxy are handles to implement later