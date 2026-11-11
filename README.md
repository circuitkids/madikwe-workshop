# Madikwe's Workshop

Queen Madikwe's video workshop, part of [BOMA](https://boma.pages.dev) (home of the Pack, a Circuit Kids project).

She writes the story; this repo renders it into a short paper-cut film with a Kokoro voice, on GitHub Actions, for free. The finished MP4 lands back in BOMA's Video Workshop card as a GitHub Release on this repo.

## How a clip is made

1. BOMA calls **Actions → Render a story clip → Run workflow** (or the `workflow_dispatch` API) with:
   - `title` - the film title (max 70 characters)
   - `script` - the narration, one spoken line per scene, 1 to 12 lines
   - `voice` - a [Kokoro](https://github.com/hexgrad/kokoro) voice (default `af_heart`)
2. The job builds a film with the open-source [Lemo-Opuscar](https://github.com/lemomo-ai/lemo-opuscar) toolbox (pinned at `9eb7739`): Kokoro TTS per line, a deterministic canvas paper-cut world (title card, savanna / dusk / night scenes, subtitle band), procedural paper foley and a wind bed, muxed with ffmpeg 7 to −14 LUFS.
3. The MP4 and a poster frame are attached to a new release `clip-<run id>`. BOMA lists those releases in its Video Workshop card.

## Layout

- `.github/workflows/render.yml` - the one-job pipeline
- `template/` - the film: `index.html` (the paper world), `make_lines.py`, `make_content.py` (timeline), `mix.py` (sound), `build.sh` (the pipeline)

No secrets live in this repo. Everything here is public by choice: GitHub is about sharing.

## Run it by hand

Actions → Render a story clip → Run workflow. Clips appear under Releases in a few minutes.
