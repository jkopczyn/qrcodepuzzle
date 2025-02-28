from typing import List, Tuple, Optional
import random
import copy
from dataclasses import dataclass

@dataclass
class MosaicPuzzle:
    width: int
    height: int
    grid: List[List[bool]]  # True = black, False = white
    clues: List[List[Optional[int]]]  # None = no clue
    
    @classmethod
    def generate_random(cls, width: int, height: int) -> 'MosaicPuzzle':
        """Generate a random puzzle with all cells filled and all clues computed"""
        grid = [[random.choice([True, False]) for _ in range(width)] 
                for _ in range(height)]
        clues = bool_grid_to_counts(grid)  # Using existing function
        return cls(width, height, grid, clues)
    
    def remove_clue(self, x: int, y: int) -> None:
        """Remove clue at position (x,y)"""
        self.clues[y][x] = None
    
    def restore_clue(self, x: int, y: int) -> None:
        """Recompute and restore clue at position (x,y)"""
        self.clues[y][x] = count_adjacent_ones(self.grid, y, x)  # Using existing function 