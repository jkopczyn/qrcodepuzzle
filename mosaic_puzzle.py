from typing import List, Tuple, Optional
import random
import copy
from dataclasses import dataclass

from bool_grid_to_count_grid import bool_grid_to_count_grid
import file_io

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
    def from_file(cls, count_grid_filename: str, boolean_grid_filename: Optional[str] = None):
        existing_puzzle = file_io.load_count_grid(count_grid_filename)
        # Convert count grid to MosaicPuzzle
        width: int = len(existing_puzzle[0])
        height: int = len(existing_puzzle)
        if boolean_grid_filename:
            grid = file_io.load_boolean_grid(boolean_grid_filename)
        else:
            grid: List[List[bool]] = [[False] * width for _ in range(height)]  # default to empty
        return cls(width, height, grid, existing_puzzle)

    def to_file(self, count_grid_filename: str, boolean_grid_filename: Optional[str] = None):
        file_io.save_count_grid(self.clues, count_grid_filename)
        if boolean_grid_filename:
            file_io.save_boolean_grid(self.grid, boolean_grid_filename)

    @classmethod
    def generate_random(cls, width: int, height: int) -> 'MosaicPuzzle':
        """Generate a random puzzle with all cells filled and all clues computed"""
        grid = [[random.choice([True, False]) for _ in range(width)]
                for _ in range(height)]
        clues = bool_grid_to_count_grid(grid)
        return cls(width, height, grid, clues)

    def remove_clue(self, x: int, y: int) -> None:
        """Remove clue at position (x,y)"""
        self.clues[y][x] = None

    def restore_clue(self, x: int, y: int) -> None:
        """Recompute and restore clue at position (x,y)"""
        self.clues[y][x] = self.original_clues[y][x]

    def count_squares(self) -> Tuple[int, int]:
        """Count the number of black and white squares in the puzzle"""
        black, white = 0, 0
        for row in self.grid:
            full = len(row)
            black_row = sum(row)
            white_row = full - black_row
            black += black_row
            white += white_row
        return black, white
