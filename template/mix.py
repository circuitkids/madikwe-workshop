#!/usr/bin/env python3
"""Mix: Kokoro voice lines + paper foley + soft wind bed -> work/out/mix.wav
Run from anywhere; reads events.json and work/content.json next to this file."""
import os, sys, json, numpy as np, soundfile as sf, soxr

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, 'work')
LIB = os.environ['LIB']
sys.path.insert(0, os.path.join(LIB, 'core/audio'))
from sfx import SR, add, brown, lp, compress, limit, pop, whoosh, ding, noise, t_

E = json.load(open(os.path.join(HERE, 'events.json')))
C = json.load(open(os.path.join(WORK, 'content.json'), encoding='utf-8'))
DUR = E['dur']
N = int(DUR * SR) + SR
buf = np.zeros((N, 2), dtype=np.float64)

# wind-through-grass bed: brown noise, low-passed, slowly breathing
bed = lp(brown(DUR + 1), 320) * (0.5 + 0.5 * np.sin(2 * np.pi * t_(DUR + 1) / 7.0)) * 0.05
add(buf, bed, 0, gain=1.0)

# foley from the timeline
for e in E['ev']:
    if e['type'] == 'pop':
        add(buf, pop(0.5), e['t'])
    elif e['type'] == 'swish':
        add(buf, whoosh(0.4, 0.35), e['t'])
    elif e['type'] == 'ding':
        add(buf, ding(0.5), e['t'])

# voice
for sc in C['scenes']:
    wav = os.path.join(WORK, 'voices', sc['voice'] + '.wav')
    a, sr = sf.read(wav)
    if a.ndim > 1: a = a.mean(axis=1)
    if sr != SR: a = soxr.resample(a, sr, SR)
    a = a / max(1e-9, np.abs(a).max()) * 0.85
    add(buf, a, sc['voice_at'])

mix = compress(buf[:, 0] * 0.6 + buf[:, 1] * 0.6)
mix = np.stack([limit(buf[:, 0]), limit(buf[:, 1])], axis=1)
os.makedirs(os.path.join(WORK, 'out'), exist_ok=True)
sf.write(os.path.join(WORK, 'out', 'mix.wav'), (mix * 0.9).astype(np.float32), SR)
print('mix: %.1fs written' % DUR)
