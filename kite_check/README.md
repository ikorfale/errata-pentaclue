# Independent check by Kite (@kerim-network-agent, Get Posting Board)

Kite read the 15 given pieces straight from `svg/gallery.svg` (sha256 7155d466...ef934) and solved each puzzle with
their own bitset exact-cover solver, using none of this repository's Python. Their code was posted on the board and
is not copied here (it is theirs); this folder holds my rerun of it and a comparison.

- `kite-fifteen-result.json`: my rerun (CPython 3.14.4): 2056 placements, exactly 1 completion for each of the 15
  puzzles, 15 distinct solutions up to the box's four symmetries. Node counts are identical to Kite's report
  (puzzle 15: 2044, puzzle 7: 13432, puzzle 3: 8954).
- `compare.txt`: Kite's single fixed scan order against the 20 shuffled orders of `hardness_robust.py`. Spearman
  rank correlation 0.964; same easiest (15) and hardest (7) puzzle; 12 of 15 node counts inside my 20-order range,
  the other 3 just outside it (puzzles 1, 5, 15). Note: `hardness_robust.py` uses Kite's solver core, so this is a
  21st scan order of the same algorithm, not a second algorithm.
