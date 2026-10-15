#!/usr/bin/env python3
"""For each tiling S of the 6x10 box: the fewest pieces of S, placed exactly as in S, that leave S as the only
completion. A clue set C works iff no other tiling T contains every placement of C.
Reads solutions.json (all 9356 oriented tilings), writes clues.json and prints the distribution."""
import itertools, json, collections
sols = json.load(open('solutions.json'))
P = 'FILNPTUVWXYZ'
key = [{p: tuple(cs) for p, cs in s} for s in sols]
# index: placement -> tilings containing it
by = collections.defaultdict(set)
for i, k in enumerate(key):
    for p in P:
        by[(p, k[p])].add(i)
out = []
for i, k in enumerate(key):
    # shared mask per other tiling, kept maximal only
    masks = {0}  # tilings sharing no placement with S rule out the empty clue set
    for p in P:
        for j in by[(p, k[p])]:
            if j != i:
                masks.add(sum(1 << P.index(q) for q in P if key[j][q] == k[q]))
    masks = [m for m in masks if not any(m != n and m & n == m for n in masks)]
    best = None
    for n in range(0, 13):
        good = [c for c in itertools.combinations(range(12), n)
                if not any(sum(1 << x for x in c) & m == sum(1 << x for x in c) for m in masks)]
        if good:
            best = (n, len(good), [''.join(P[x] for x in c) for c in good]); break
    out.append({'i': i, 'min': best[0], 'n_sets': best[1], 'sets': best[2][:50], 'others_sharing': len(masks)})
json.dump(out, open('clues.json', 'w'))
d = collections.Counter(o['min'] for o in out)
print('fewest clues needed -> tilings (of', len(out), 'oriented):', dict(sorted(d.items())))
