#!/usr/bin/env python3
"""Robustness of the hardness ranking: same solver, cell scan order randomly permuted (20 seeds per puzzle).
A ranking that flips with the scan order is a property of the solver, not of the puzzle."""
import json, random, statistics
import hardness as H  # runs hardness.py's module-level loop once; cheap
def nodes(fixed, order):
    n = [0]
    def solve(rem, av):
        n[0] += 1
        if not rem: return
        best, bc = 0, 10 ** 9
        for c in order:
            if rem >> c & 1:
                o = H.cols[c] & av; k = o.bit_count()
                if k < bc:
                    best, bc = o, k
                    if k <= 1: break
        while best:
            b = best & -best; ri = b.bit_length() - 1
            solve(rem & ~H.rows[ri], av & ~H.conf[ri]); best ^= b
    solve(((1 << 72) - 1) & ~H.rows[fixed], ((1 << len(H.rows)) - 1) & ~H.conf[fixed])
    return n[0]
sols = json.load(open('solutions.json'))
res = []
for pz in json.load(open('one_clue.json')):
    sol = {p: tuple(sorted(cs)) for p, cs in sols[pz['i']]}
    fixed = next(k for k in range(len(H.rows)) if H.labels[k] == pz['clue'] and H.coords[k] == sol[pz['clue']])
    v = []
    for seed in range(20):
        order = list(range(72)); random.Random(seed).shuffle(order); v.append(nodes(fixed, order))
    res.append({'i': pz['i'], 'clue': pz['clue'], 'median': statistics.median(v), 'min': min(v), 'max': max(v)})
    print(json.dumps(res[-1]), flush=True)
json.dump(res, open('hardness_robust.json', 'w'), indent=1)
