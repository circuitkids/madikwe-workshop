#!/usr/bin/env python3
"""Build lines.json (one Kokoro line per narration line) from the job inputs."""
import argparse, json, os, re, sys

p = argparse.ArgumentParser()
p.add_argument('--title', required=True)
p.add_argument('--script', required=True, help='text file, one narration line per line')
p.add_argument('--voice', default='af_heart')
p.add_argument('--speed', type=float, default=0.95)
p.add_argument('--dir', required=True)
a = p.parse_args()

os.makedirs(os.path.join(a.dir, 'voices'), exist_ok=True)
title = re.sub(r'\s+', ' ', a.title).strip()
if not title: sys.exit('make_lines: empty title')
if len(title) > 70: sys.exit('make_lines: title too long (max 70 characters)')

raw = [re.sub(r'\s+', ' ', ln).strip() for ln in open(a.script, encoding='utf-8').read().splitlines()]
texts = [ln for ln in raw if ln]
if not (1 <= len(texts) <= 12): sys.exit('make_lines: need 1-12 narration lines, got %d' % len(texts))
for ln in texts:
    if len(ln) > 220: sys.exit('make_lines: one line is over 220 characters: ' + ln[:40])

lines = [{'id': 'l%d' % (i + 1), 'text': t, 'voice': a.voice, 'speed': a.speed} for i, t in enumerate(texts)]
json.dump(lines, open(os.path.join(a.dir, 'lines.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
json.dump({'title': title}, open(os.path.join(a.dir, 'job.json'), 'w'))
print('make_lines: %d lines, title "%s"' % (len(lines), title))
