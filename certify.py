#!/usr/bin/env python3
"""Independent check of one puzzle with a SAT solver, not with the enumeration.
certify.py I CLUES: tiling I from solutions.json, CLUES = pieces fixed as in that tiling (e.g. "IX").
Encodes every legal placement of the 12 pentominoes in the 6x10 box (placements rebuilt here, not read from
enum.py), each cell covered exactly once, each piece used exactly once, the clues as unit clauses.
Run 1: the solution itself must be SAT (control). Run 2: add a clause forbidding tiling I -> must be UNSAT,
with a DRAT proof checked by drat-trim. Run 3 (control): drop one clue -> must be SAT (another completion)."""
import json, subprocess, sys, itertools
W, H = 10, 6
BASE = {'F': '.##|##.|.#.', 'I': '#|#|#|#|#', 'L': '#.|#.|#.|##', 'N': '.#|.#|##|#.', 'P': '##|##|#.',
        'T': '###|.#.|.#.', 'U': '#.#|###', 'V': '#..|#..|###', 'W': '#..|##.|.##', 'X': '.#.|###|.#.',
        'Y': '.#|##|.#|.#', 'Z': '##.|.#.|.##'}
def shapes(pic):
    cells = [(r, c) for r, row in enumerate(pic.split('|')) for c, ch in enumerate(row) if ch == '#']
    out = set()
    for f in (1, -1):
        for k in range(4):
            cs = [(r, f * c) for r, c in cells]
            for _ in range(k):
                cs = [(c, -r) for r, c in cs]
            mr, mc = min(r for r, c in cs), min(c for r, c in cs)
            out.add(tuple(sorted((r - mr, c - mc) for r, c in cs)))
    return out
pl = []
for p, pic in BASE.items():
    for o in shapes(pic):
        for dr in range(H):
            for dc in range(W):
                cs = tuple(sorted((r + dr) * W + c + dc for r, c in o))
                if all(r + dr < H and c + dc < W for r, c in o):
                    pl.append((p, cs))
var = {x: i + 1 for i, x in enumerate(pl)}
def exactly_one(vs):
    return [list(vs)] + [[-a, -b] for a, b in itertools.combinations(vs, 2)]
base = []
for cell in range(W * H):
    base += exactly_one([var[x] for x in pl if cell in x[1]])
for p in BASE:
    base += exactly_one([var[x] for x in pl if x[0] == p])
def run(clauses, name, proof=False):
    n = len(pl)
    open(name + '.cnf', 'w').write(f'p cnf {n} {len(clauses)}\n' + ''.join(' '.join(map(str, c)) + ' 0\n' for c in clauses))
    cmd = ['kissat', '-q', name + '.cnf'] + ([name + '.drat', '--no-binary'] if proof else [])
    rc = subprocess.run(cmd, capture_output=True).returncode
    res = {10: 'SAT', 20: 'UNSAT'}.get(rc, f'rc{rc}')
    if proof and res == 'UNSAT':
        out = subprocess.run(['drat-trim', name + '.cnf', name + '.drat'], capture_output=True, text=True).stdout
        res += ' drat-trim:' + ('VERIFIED' if 's VERIFIED' in out else 'FAILED')
    return res
i, clues = int(sys.argv[1]), sys.argv[2]
sol = {p: tuple(cs) for p, cs in json.load(open('solutions.json'))[i]}
units = [[var[(p, sol[p])]] for p in clues]
block = [[-var[(p, sol[p])] for p in BASE]]
tag = f'cert_{i}_{clues}'
print(len(pl), 'placements;', 'solution itself:', run(base + units, tag + '_ctl'))
print('another completion:', run(base + units + block, tag, proof=True))
for p in clues:
    print(f'without clue {p}:', run(base + [u for u in units if u != [var[(p, sol[p])]]] + block, tag + '_drop'))
