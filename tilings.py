#!/usr/bin/env python3
"""Enumerate every tiling of the 6x10 rectangle by the 12 pentominoes (Algorithm X).
Writes solutions.json: a list of tilings, each a list of 12 [piece, sorted cell indices]; cell = r*10+c.
Every rotation/reflection of the board is a separate tiling here (expect 4 x 2339 = 9356)."""
import json, sys, time
W, H = 10, 6
SHAPES = {  # one orientation each, (row, col)
 'F': [(0,1),(0,2),(1,0),(1,1),(2,1)], 'I': [(0,0),(1,0),(2,0),(3,0),(4,0)],
 'L': [(0,0),(1,0),(2,0),(3,0),(3,1)], 'N': [(0,1),(1,1),(2,0),(2,1),(3,0)],
 'P': [(0,0),(0,1),(1,0),(1,1),(2,0)], 'T': [(0,0),(0,1),(0,2),(1,1),(2,1)],
 'U': [(0,0),(0,2),(1,0),(1,1),(1,2)], 'V': [(0,0),(1,0),(2,0),(2,1),(2,2)],
 'W': [(0,0),(1,0),(1,1),(2,1),(2,2)], 'X': [(0,1),(1,0),(1,1),(1,2),(2,1)],
 'Y': [(0,1),(1,0),(1,1),(2,1),(3,1)], 'Z': [(0,0),(0,1),(1,1),(2,1),(2,2)]}

def orients(cells):
    out, cur = set(), cells
    for flip in range(2):
        for rot in range(4):
            cur = [(c, -r) for r, c in cur]
            mr, mc = min(r for r, c in cur), min(c for r, c in cur)
            out.add(tuple(sorted((r - mr, c - mc) for r, c in cur)))
        cur = [(r, -c) for r, c in cur]
    return out

rows = []  # (piece, cells)
for p, s in SHAPES.items():
    for o in orients(s):
        for dr in range(H):
            for dc in range(W):
                cs = [(r + dr, c + dc) for r, c in o]
                if all(r < H and c < W for r, c in cs):
                    rows.append((p, tuple(sorted(r * W + c for r, c in cs))))
X = {}
for i, (p, cs) in enumerate(rows):
    for col in (p,) + cs:
        X.setdefault(col, set()).add(i)
Y = {i: (p,) + cs for i, (p, cs) in enumerate(rows)}

def select(r):
    cols = []
    for j in Y[r]:
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].remove(i)
        cols.append(X.pop(j))
    return cols

def deselect(r, cols):
    for j in reversed(Y[r]):
        X[j] = cols.pop()
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)

sols, part = [], []
def solve():
    if not X:
        sols.append([[rows[i][0], list(rows[i][1])] for i in part]); return
    c = min(X, key=lambda c: len(X[c]))
    for r in list(X[c]):
        part.append(r); cols = select(r); solve(); deselect(r, cols); part.pop()

t = time.time(); solve()
print(f'{len(rows)} placements, {len(sols)} tilings, {time.time()-t:.0f}s', file=sys.stderr)
json.dump(sols, open('solutions.json', 'w'))
