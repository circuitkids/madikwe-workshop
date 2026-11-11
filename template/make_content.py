#!/usr/bin/env python3
"""After TTS: lay out the timeline and write content.json for the film page."""
import argparse, json, os

p = argparse.ArgumentParser()
p.add_argument('--dir', required=True)
a = p.parse_args()

job = json.load(open(os.path.join(a.dir, 'job.json')))
lines = json.load(open(os.path.join(a.dir, 'lines.json'), encoding='utf-8'))
dur = json.load(open(os.path.join(a.dir, 'voices', 'dur.json')))

TITLE_T = 2.6
LEAD, TAIL = 0.55, 0.95   # silence around each voice line inside its scene
END_T = 3.0

ev = []
scenes = []
t = TITLE_T
ev.append({'t': 0.15, 'type': 'ding'})
for i, L in enumerate(lines):
    vd = dur[L['id']]
    sd = LEAD + vd + TAIL
    sc = {'palette': i % 3, 'start': round(t, 3), 'dur': round(sd, 3),
          'text': L['text'], 'voice': L['id'], 'voice_at': round(t + LEAD, 3), 'voice_dur': vd}
    scenes.append(sc)
    ev.append({'t': round(t, 3), 'type': 'swish'})
    for j in range(3):
        ev.append({'t': round(t + j * 0.12 + 0.28, 3), 'type': 'pop'})
    t += sd
end = {'start': round(t, 3), 'dur': END_T}
ev.append({'t': round(t + 0.1, 3), 'type': 'ding'})
t += END_T

content = {'title': job['title'], 'titleCard': {'end': TITLE_T}, 'scenes': scenes, 'end': end,
           'dur': round(t, 3), 'ev': sorted(ev, key=lambda e: e['t'])}
json.dump(content, open(os.path.join(a.dir, 'content.json'), 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
print('make_content: %.1fs, %d scenes' % (t, len(scenes)))
