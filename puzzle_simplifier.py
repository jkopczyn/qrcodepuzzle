import copy
import random
from typing import List, Tuple

from mosaic_puzzle import MosaicPuzzle
from uniqueness_checker import check_uniqueness

def simplify_puzzle(puzzle: MosaicPuzzle, next_clue_positions: List[Tuple[int, int]] = None) -> Tuple[MosaicPuzzle, List[Tuple[int, int]]]:
    """
    Remove unnecessary clues while maintaining unique solvability.
    Returns simplified puzzle.
    """
    simplified = copy.deepcopy(puzzle)

    if next_clue_positions is None:
        # Remove clues in random order, but set an order
        clue_positions: List[Tuple[int, int]] = [(x, y)
                         for y in range(puzzle.height)
                         for x in range(puzzle.width)
                         if puzzle.clues[y][x] is not None]
        random.shuffle(clue_positions)
    else:
        clue_positions = next_clue_positions


    if len(clue_positions) == 0:
        print("No more clues to remove")
        print(simplified.grid, simplified.clues, simplified.original_clues)
        return (simplified, None)

    # Try removing this clue
    x, y = clue_positions.pop()
    simplified.clues[y][x] = None

    # Check if still unique
    is_unique, _ = check_uniqueness(simplified)
    if not is_unique:
        # Restore clue if needed for uniqueness
        simplified.restore_clue(x, y)
        print("Restoring clue {} at ({}, {})".format(simplified.original_clues[y][x], x, y))

    return (simplified, clue_positions)