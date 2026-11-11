#!/bin/sh
# Madikwe's workshop: job inputs -> finished MP4.
# Needs: LIB (lemo-opuscar library root, deps+voice installed), TITLE, SCRIPT_FILE; optional VOICE, SLUG.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
: "${LIB:?set LIB to the lemo-opuscar library root}"
: "${TITLE:?}"; : "${SCRIPT_FILE:?}"
VOICE=${VOICE:-af_heart}
SLUG=$(printf '%s' "${SLUG:-clip}" | tr -cd 'a-z0-9-' | cut -c1-40)
[ -n "$SLUG" ] || SLUG=clip
PY="$LIB/.venv/bin/python"
export LIB
cd "$LIB"
"$PY" "$HERE/make_lines.py" --title "$TITLE" --script "$SCRIPT_FILE" --voice "$VOICE" --dir "$HERE/work"
"$PY" core/tts/tts.py "$HERE/work/lines.json" "$HERE/work/voices"
"$PY" "$HERE/make_content.py" --dir "$HERE/work"
node core/render/events.mjs "$HERE" --q 'content=work/content.json'
node core/render/video.mjs "$HERE" --q 'content=work/content.json' --fps 12 --size 1280x720 --workers 4 --out "$HERE/work/out/video.mp4"
"$PY" "$HERE/mix.py"
sh core/render/mux.sh "$HERE/work/out/video.mp4" "$HERE/work/out/mix.wav" "$HERE/work/out/$SLUG.mp4" 12 1
node core/render/still.mjs "$HERE" 1.3 --q 'content=work/content.json' --out "$HERE/work/stills" --prefix poster_
mv "$HERE/work/stills/poster_1.3.jpg" "$HERE/work/out/poster.jpg" 2>/dev/null || true
ls -la "$HERE/work/out/"
