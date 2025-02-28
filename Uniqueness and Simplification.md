Mosaic as a SAT problem
Author:
Thijs de Jong
s1015438

Chapter 4
Generating puzzles
4.1 Checking if a puzzle has a unique solution
In order to be able to generate uniquely solvable puzzles, we need to be able
to check if a given configuration of a puzzle is unique. This can be done
by adding the boolean formula that states that the known solution is not
a possible solution anymore for this configuration to the encoding of the
mosaic puzzle. This can be seen as ’blocking’ the actual solution from being
a solution. With this, we can check whether the current configuration of the
game is uniquely solvable. If the CNF is satisfiable, there is another solution
for the game, making it nonunique. This can be done at any given point in
the generation process.
Example 4.1.1. Suppose we have a simple original configuration, shown in
figure 4.1, for which we want to check whether it is unique.
Figure 4.1: Simple starting configuration of a Mosaic
To do so, we need to add the boolean formula that states that the cur-
rent correct solution is not possible anymore as a solution. This way, if
the SAT solver evaluates the encoded puzzle to unsatisfiable, there is no
other solution, and the configuration of the puzzle is unique. If the SAT
solver evaluates the encoded puzzle to satisfiable, together with a list of
which variables have to be true and which false, there is another solution
next to the known solution.

4.2 Generating puzzles using the SAT encoding
In order to generate a puzzle, some steps have to be taken. First, a grid has
to be generated of any chosen size, where every cell in the grid is either black
or white. This will be determined randomly. After that, for every cell, the
correct clue value will be filled in, depending on the number of black cells
surrounding the cell, including the cell itself. Once the entire grid is filled
with clues, we first check whether the original solution is unique using the
method described in chapter 4.1. If this is not the case, we will regenerate
the starting grid and the corresponding clues, until we have found a unique
original solution.
We can now check for every cell whether the clue is important for a
unique solution, so that we can remove clues in order to get a puzzle with
the least number of clues needed. For every cell in the puzzle, we will try to
remove the clue in the cell from the puzzle, and try to evaluate the encoding
of the puzzle with the SAT solver again. If the SAT solver can’t find a
solution, the puzzle is still uniquely solvable, since the correct solution is
blocked, so the clue will stay removed. If it can find a solution, the clue
will be put back in the puzzle, as this clue is important for making the
puzzle uniquely solvable. This will be done for every cell in the puzzle,
going from left to right, from top to bottom. When for every cell it has been
checked whether the clue is important for the unique solutions, the result is
a configuration of the Mosaic puzzle that is uniquely solvable.
Example 4.2.1. In this example, we will show the steps taken to generate
a Mosaic puzzle. The size of the puzzle that will be generated is 5x5. To
start with, we will set every cell in the 5x5 grid to black or white randomly.
The result can be seen in figure 4.5.
Figure 4.5: Setting all cells randomly to either black or white
After this is done, we will fill every cell in the 5x5 grid with its cor-
responding clue. This can be done by counting the number of black cells
surrounding the cell, including the cell itself. The result of this can be seen
in figure 4.6.
Figure 4.6: Computing the clues for all cells
Now that we have a basic configuration of the Mosaic, we first check
whether this original configuration is unique according to chapter 4.1, which
is the case. After this, we can start with the removal of the clues that are
not necessary for a unique solution. We will try to remove clues one by one,
convert the new configuration to an encoding, and try to solve this encoding
with a SAT solver. This will be done from left to right, top to bottom.
The clue of the first cell with coordinates (0,0) can be removed, as can be
seen in figure 4.7a, since without this clue, the configuration is still uniquely
solvable, as the SAT solver evaluates to unsatisfiable. The same goes for
the second cell, with coordinates (1,0), as can be seen in figure 4.7b.
Figure 4.7: The first clues can be removed since the new configuration is
still uniquely solvable without them
We can continue this removal of clues until the 7th cell. At this cell,
with coordinates (1,1), we can see that upon removal, a solution other
than the original solution is possible. The original solution can be seen in
figure 4.8a, and the new solution, found by the SAT solver, in figure 4.8b.
The red cell is the cell from which the clue got removed. The top left cell,
on coordinates (0,0), can be either black or white, without interfering with
any clue, meaning that the clue in the cell on coordinates (1,1) is important
for a unique solution. We can continue the removal of clues this way to end
up with a uniquely solvable configuration of a Mosaic puzzle, which can be
seen in figure 4.9.
Figure 4.8: Two different solutions are possible upon removal of the clue in
the cell indicated with red
Figure 4.9: A uniquely solvable generated configuration of a Mosaic puzzle