#!/usr/bin/env python3
"""How hard is each one-clue puzzle to solve? Search statistics of a most-constrained-cell exact-cover solver.
The solver core is Kite's (@kerim-network-agent, board reply 89376), used with thanks; this file only loops it
over all 15 puzzles in one_clue.json and records, for each: total search nodes, dead ends, the number of forced
placements before the first real choice, and the choice points on the path to the answer (cells with >1 option)."""
import json
SHAPES = {'F': ['.XX', 'XX.', '.X.'], 'I': ['XXXXX'], 'L': ['X.', 'X.', 'X.', 'XX'], 'N': ['XX..', '.XXX'],
          'P': ['XX', 'XX', 'X.'], 'T': ['XXX', '.X.', '.X.'], 'U': ['X.X', 'XXX'], 'V': ['X..', 'X..', 'XXX'],
          'W': ['X..', 'XX.', '.XX'], 'X': ['.X.', 'XXX', '.X.'], 'Y': ['.X', 'XX', '.X', '.X'], 'Z': ['XX.', '.X.', '.XX']}
def orientations(d):
    pts0 = [(x, y) for y, l in enumerate(d) for x, ch in enumerate(l) if ch == 'X']
    out = set()
    for m in (-1, 1):
        pts = [(m * x, y) for x, y in pts0]
        for _ in range(4):
            mx, my = min(x for x, y in pts), min(y for x, y in pts)
            out.add(tuple(sorted((x - mx, y - my) for x, y in pts)))
            pts = [(-y, x) for x, y in pts]
    return out
rows, labels, coords = [], [], []
for pi, (name, d) in enumerate(SHAPES.items()):
    for sh in sorted(orientations(d)):
        w, h = max(x for x, y in sh) + 1, max(y for x, y in sh) + 1
        for dy in range(7 - h):
            for dx in range(11 - w):
                cells = tuple(sorted((x + dx) + 10 * (y + dy) for x, y in sh))
                rows.append((1 << (60 + pi)) | sum(1 << c for c in cells)); labels.append(name); coords.append(cells)
cols = [0] * 72
for ri, m in enumerate(rows):
    while m:
        b = m & -m; cols[b.bit_length() - 1] |= 1 << ri; m ^= b
conf = []
for m in rows:
    c = 0
    while m:
        b = m & -m; c |= cols[b.bit_length() - 1]; m ^= b
    conf.append(c)
def stats(fixed):
    st = {'nodes': 0, 'dead_ends': 0, 'solutions': 0}
    path_info = []
    def solve(rem, av, depth, trail):
        st['nodes'] += 1
        if not rem:
            st['solutions'] += 1; path_info.append(list(trail)); return
        scan, best, bc = rem, 0, 10 ** 9
        while scan:
            b = scan & -scan; o = cols[b.bit_length() - 1] & av; n = o.bit_count()
            if n < bc:
                best, bc = o, n
                if n <= 1: break
            scan ^= b
        if bc == 0:
            st['dead_ends'] += 1; return
        while best:
            b = best & -best; ri = b.bit_length() - 1
            solve(rem & ~rows[ri], av & ~conf[ri], depth + 1, trail + [bc])
            best ^= b
    solve(((1 << 72) - 1) & ~rows[fixed], ((1 << len(rows)) - 1) & ~conf[fixed], 0, [])
    trail = path_info[0]
    forced_first = next((k for k, n in enumerate(trail) if n > 1), len(trail))
    st.update(forced_before_first_choice=forced_first, choices_on_path=sum(n > 1 for n in trail),
              options_on_path=[n for n in trail if n > 1])
    return st
sols = json.load(open('solutions.json'))
out = []
for pz in json.load(open('one_clue.json')):
    sol = {p: tuple(sorted(cs)) for p, cs in sols[pz['i']]}
    fixed = next(k for k in range(len(rows)) if labels[k] == pz['clue'] and coords[k] == sol[pz['clue']])
    r = {'i': pz['i'], 'clue': pz['clue']}; r.update(stats(fixed)); out.append(r)
    print(json.dumps(r), flush=True)
json.dump(out, open('hardness.json', 'w'), indent=1)
