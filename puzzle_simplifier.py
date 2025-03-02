import copy
import random
from typing import List, Tuple

from mosaic_puzzle import MosaicPuzzle
from uniqueness_checker import check_uniqueness

def randomize_clue_order(puzzle: MosaicPuzzle) -> List[Tuple[int, int]]:
    clue_positions: List[Tuple[int, int]] = [(x, y)
                         for y in range(puzzle.height)
                         for x in range(puzzle.width)
                         if puzzle.clues[y][x] is not None]
    random.shuffle(clue_positions)
    return clue_positions

def simplify_puzzle(puzzle: MosaicPuzzle, clue_order: List[Tuple[int, int]] = None) -> Tuple[MosaicPuzzle, List[Tuple[int, int]]]:
    """
    Remove unnecessary clues while maintaining unique solvability.
    Returns simplified puzzle.
    """
    simplified = copy.deepcopy(puzzle)

    if clue_order is None:
        # Remove clues in random order, but set an order
        clue_order = randomize_clue_order(puzzle)

    if len(clue_order) == 0:
        print("No more clues to remove")
        print(simplified.grid, simplified.clues, simplified.original_clues)
        return (simplified, None)

    # Try removing this clue
    x, y = clue_order.pop()
    simplified.clues[y][x] = None

    # Check if still unique
    is_unique, alt_solution = check_uniqueness(simplified)
    if not is_unique:
        # Restore clue if needed for uniqueness
        simplified.restore_clue(x, y)
        print("Restoring clue {} at ({}, {})".format(simplified.original_clues[y][x], x, y))

    return (simplified, clue_order)