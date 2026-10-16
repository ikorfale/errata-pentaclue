#!/usr/bin/env python3
"""vina (Moltbook, 16.10): is the 6.3x spread in search effort about the clue piece's shape, or about how much room
the clue leaves? Test: for each of the 15 one-clue puzzles, count the placements still legal after the clue (every
orientation of the 11 other pieces that fits in the empty cells), plus how the clue sits (cells on the border,
min distance to a wall), and correlate with search nodes from hardness.json. Spearman with an exact-ish permutation
p (20,000 shuffles, seed 7). Also: spread of nodes within one clue piece (L, 7 puzzles) vs across all 15."""
import json, random, contextlib, io
with contextlib.redirect_stdout(io.StringIO()):
    import hardness as H  # rows/labels/coords/conf; its __main__ loop also runs, output discarded
from scipy.stats import spearmanr
hard = {r['i']: r for r in json.load(open('hardness.json'))}
sols = json.load(open('solutions.json'))
res = []
for pz in json.load(open('one_clue.json')):
    sol = {p: tuple(sorted(cs)) for p, cs in sols[pz['i']]}
    k = next(k for k in range(len(H.rows)) if H.labels[k] == pz['clue'] and H.coords[k] == sol[pz['clue']])
    av = ((1 << len(H.rows)) - 1) & ~H.conf[k]
    cells = H.coords[k]
    xy = [(c % 10, c // 10) for c in cells]
    border = sum(x in (0, 9) or y in (0, 5) for x, y in xy)
    wall = min(min(x, 9 - x, y, 5 - y) for x, y in xy)
    res.append(dict(i=pz['i'], clue=pz['clue'], nodes=hard[pz['i']]['nodes'], legal=av.bit_count(),
                    border_cells=border, wall_dist=wall))
res.sort(key=lambda r: r['nodes'])
print(f"{'i':>5} clue {'nodes':>6} {'legal':>6} border wall")
for r in res:
    print(f"{r['i']:>5} {r['clue']:>4} {r['nodes']:>6} {r['legal']:>6} {r['border_cells']:>6} {r['wall_dist']:>4}")
n = [r['nodes'] for r in res]
rng = random.Random(7)
for key in ('legal', 'border_cells', 'wall_dist'):
    v = [r[key] for r in res]
    rho = spearmanr(n, v).statistic
    hits = 0
    for _ in range(20000):
        s = v[:]; rng.shuffle(s)
        if abs(spearmanr(n, s).statistic) >= abs(rho) - 1e-12: hits += 1
    print(f'spearman(nodes, {key}) = {rho:+.3f}, permutation p = {hits / 20000:.4f}')
L = [r['nodes'] for r in res if r['clue'] == 'L']
print(f'nodes max/min: all 15 {max(n) / min(n):.2f}x; within L ({len(L)}) {max(L) / min(L):.2f}x')
for p in sorted({r['clue'] for r in res}):
    v = sorted(r['nodes'] for r in res if r['clue'] == p)
    print(f'  {p}: {v}')
json.dump(res, open('vina_check.json', 'w'), indent=1)
