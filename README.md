# QR-Mosaic

I played a particular puzzle, [Mosaic](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/mosaic.html), from the Simon Tatham collection and it occurred to me that you could turn an arbitrary QR code into a valid solvable puzzle of that type.

## To use:
1. Clone repository.
2a. If you have a QR code already in mind, move the image (as PNG) into the directory and call `python image_to_puzzle.py <imagefilename>`.
2b. If you have a secret code instead, `./secret_to_puzzle.sh <secret_code>`.

In either case note that the time to prune the puzzle to a reasonable density of clues grows, I believe, with $$O(n^7)$$, where n is the side length of the QR grid square. The smallest size, 21x21, takes about four minutes on my reasonably-powerful laptop, and a 21-character pure alphanumeric clue like 'Sufficiently Analyzed' is the longest it can hold; a slightly longer clue or one with nontrivial punctuation takes fifteen minutes. An 140-character tweet (37x37) would take at least several hours, and a day or more is possible; 280 characters (45x45) will take at least half a day and possibly several days.

I do not expect _significant_ efficiency gains are achievable but tweaks around the edges might get it down to a quarter the current time and put old-length tweets in reasonable reach.
