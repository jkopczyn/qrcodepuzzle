import copy
import random
from typing import List, Tuple

from mosaic_puzzle import MosaicPuzzle
from uniqueness_checker import check_uniqueness

def simplify_puzzle(puzzle: MosaicPuzzle) -> MosaicPuzzle:
    """
    Remove unnecessary clues while maintaining unique solvability.
    Returns simplified puzzle.
    """
    simplified = copy.deepcopy(puzzle)
    
    # Try removing clues in random order to avoid bias
    clue_positions: List[Tuple[int, int]] = [(x, y) 
                     for y in range(puzzle.height) 
                     for x in range(puzzle.width) 
                     if puzzle.clues[y][x] is not None]
    random.shuffle(clue_positions)
    
    for x, y in clue_positions:
        # Try removing this clue
        simplified.remove_clue(x, y)
        
        # Check if still unique
        is_unique, _ = check_uniqueness(simplified)
        if not is_unique:
            # Restore clue if needed for uniqueness
            simplified.restore_clue(x, y)
    
    return simplified 