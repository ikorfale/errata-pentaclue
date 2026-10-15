#!/usr/bin/env python3
"""gallery.py: the 15 tilings (up to turning/flipping the box) that a single placed piece forces.
Writes one_clue.json (one representative per symmetry class) and svg/gallery.svg (puzzles) and
svg/gallery-solutions.svg."""
import json
W, H = 10, 6
sols = json.load(open('solutions.json')); cl = json.load(open('clues.json'))
def img(s, f):  # cell -> piece under a box symmetry f
    return tuple(sorted((f(c), p) for p, cs in s for c in cs))
syms = [lambda c: c, lambda c: (c // W) * W + (W - 1 - c % W), lambda c: (H - 1 - c // W) * W + c % W,
        lambda c: (H - 1 - c // W) * W + (W - 1 - c % W)]
seen, reps = set(), []
for o in cl:
    if o['min'] != 1: continue
    s = sols[o['i']]
    can = min(img(s, f) for f in syms)
    if can in seen: continue
    seen.add(can); reps.append({'i': o['i'], 'clue': o['sets'][0]})
json.dump(reps, open('one_clue.json', 'w'), indent=1)
import subprocess, re
for kind in ('', '-solutions'):
    parts, cols = [], 3
    for k, r in enumerate(reps):
        subprocess.run(['python3', 'draw.py', str(r['i']), r['clue'], '/tmp/pc.svg', '--notray'] + (['--solution'] if kind else []), check=True)
        body = open('/tmp/pc.svg').read()
        w, h = map(int, re.search(r'width="(\d+)" height="(\d+)"', body).groups())
        inner = body.split('>', 1)[1].rsplit('</svg>', 1)[0]
        x, y = (k % cols) * w, (k // cols) * (h + 22)
        parts.append(f'<g transform="translate({x},{y + 22})">{inner}</g>')
        parts.append(f'<text x="{x + 20}" y="{y + 30}" font-size="13" fill="#444" font-family="Georgia,serif">{k + 1}. given: {r["clue"]}</text>')
    W2, H2 = cols * w, -(-len(reps) // cols) * (h + 22) + 22
    open(f'svg/gallery{kind}.svg', 'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W2}" height="{H2}" viewBox="0 0 {W2} {H2}"><rect width="{W2}" height="{H2}" fill="#faf7f0"/>' + ''.join(parts) + '</svg>')
print(len(reps), 'one-clue puzzles:', ' '.join(r['clue'] for r in reps))
