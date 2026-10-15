#!/usr/bin/env python3
"""draw.py I CLUES OUT.svg [--solution]: the 6x10 box with the clue pieces placed, the other cells empty,
and the pieces still to place drawn underneath. --solution fills every piece."""
import json, sys
W, H, S = 10, 6, 40
COL = {'F': '#c8553d', 'I': '#2d7dd2', 'L': '#97cc04', 'N': '#f45d01', 'P': '#7d5ba6', 'T': '#e3b505',
       'U': '#0e9594', 'V': '#d64996', 'W': '#5c8001', 'X': '#8c2f39', 'Y': '#3a506b', 'Z': '#b07d48'}
BASE = {'F': '.##|##.|.#.', 'I': '#####', 'L': '####|#...', 'N': '##..|.###', 'P': '##|##|#.',
        'T': '###|.#.|.#.', 'U': '#.#|###', 'V': '#..|#..|###', 'W': '#..|##.|.##', 'X': '.#.|###|.#.',
        'Y': '####|.#..', 'Z': '##.|.#.|.##'}
i, clues, out = int(sys.argv[1]), sys.argv[2], sys.argv[3]
full = '--solution' in sys.argv
notray = '--notray' in sys.argv
sol = {p: cs for p, cs in json.load(open('solutions.json'))[i]}
show = 'FILNPTUVWXYZ' if full else clues
m = 20
rest = [] if notray else [p for p in 'FILNPTUVWXYZ' if p not in show]
tray_h = 0 if not rest else 2 * 4 * 14 + 40
w, h = W * S + 2 * m, H * S + 2 * m + tray_h + (0 if notray else 24)
o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" font-family="Georgia,serif">',
     f'<rect width="{w}" height="{h}" fill="#faf7f0"/>']
for r in range(H):
    for c in range(W):
        o.append(f'<rect x="{m+c*S}" y="{m+r*S}" width="{S}" height="{S}" fill="none" stroke="#d8d2c4"/>')
owner = {cell: p for p, cs in sol.items() for cell in cs}
for p in show:
    for cell in sol[p]:
        r, c = divmod(cell, W)
        o.append(f'<rect x="{m+c*S}" y="{m+r*S}" width="{S}" height="{S}" fill="{COL[p]}"/>')
    r, c = divmod(sorted(sol[p])[2], W)
    o.append(f'<text x="{m+c*S+S/2}" y="{m+r*S+S/2+6}" text-anchor="middle" font-size="18" fill="#fff">{p}</text>')
# heavy borders between different pieces (only around shown cells) and the box outline
for cell, p in owner.items():
    if p not in show: continue
    r, c = divmod(cell, W)
    for dr, dc, x1, y1, x2, y2 in ((-1,0,0,0,1,0),(1,0,0,1,1,1),(0,-1,0,0,0,1),(0,1,1,0,1,1)):
        rr, cc = r + dr, c + dc
        if not (0 <= rr < H and 0 <= cc < W) or owner[rr*W+cc] != p:
            o.append(f'<line x1="{m+(c+x1)*S}" y1="{m+(r+y1)*S}" x2="{m+(c+x2)*S}" y2="{m+(r+y2)*S}" stroke="#222" stroke-width="2.5"/>')
o.append(f'<rect x="{m}" y="{m}" width="{W*S}" height="{H*S}" fill="none" stroke="#222" stroke-width="3"/>')
if rest:
    y0 = m + H * S + 24
    o.append(f'<text x="{m}" y="{y0}" font-size="14" fill="#444">Fill the box with the other {len(rest)} pieces (turn and flip them).</text>'
             f'<text x="{m}" y="{y0+18}" font-size="14" fill="#444">There is exactly one way.</text>')
    x, yrow = m, y0 + 32
    for p in rest:
        cells = [(r, c) for r, row in enumerate(BASE[p].split('|')) for c, ch in enumerate(row) if ch == '#']
        if x + (max(c for r, c in cells) + 1) * 14 > w - m:
            x, yrow = m, yrow + 4 * 14
        for r, c in cells:
            o.append(f'<rect x="{x+c*14}" y="{yrow+r*14}" width="13" height="13" fill="{COL[p]}"/>')
        x += (max(c for r, c in cells) + 2) * 14
o.append('</svg>')
open(out, 'w').write('\n'.join(o))
