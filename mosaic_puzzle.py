from typing import List, Tuple, Optional
import random
import copy
from dataclasses import dataclass

from bool_grid_to_count_grid import bool_grid_to_counts, count_adjacent_ones

@dataclass
class MosaicPuzzle:
    width: int
    height: int
    grid: List[List[bool]]  # True = black, False = white
    clues: List[List[Optional[int]]]  # None = no clue
    original_clues: List[List[Optional[int]]]  # None = no clue

    def __init__(self, width: int, height: int, grid: List[List[bool]], clues: List[List[Optional[int]]]):
        self.width = width
        self.height = height
        self.grid = grid
        self.clues = clues
        self.original_clues = copy.deepcopy(clues)

    @classmethod
    def generate_random(cls, width: int, height: int) -> 'MosaicPuzzle':
        """Generate a random puzzle with all cells filled and all clues computed"""
        grid = [[random.choice([True, False]) for _ in range(width)] 
                for _ in range(height)]
        clues = bool_grid_to_counts(grid)
        return cls(width, height, grid, clues)
    
    def remove_clue(self, x: int, y: int) -> None:
        """Remove clue at position (x,y)"""
        self.clues[y][x] = None
    
    def restore_clue(self, x: int, y: int) -> None:
        """Recompute and restore clue at position (x,y)"""
        self.clues[y][x] = self.original_clues[y][x]