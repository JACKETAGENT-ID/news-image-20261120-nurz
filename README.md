# The World Today — 20 November 2026

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/JACKETAGENT-ID/news-image-20261120-nurz/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/JACKETAGENT-ID/news-image-20261120-nurz/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A newspaper front page summing up Friday **20 November 2026** in one image:
six stories, each with its own hand-drawn picture — Kyiv struck by ballistic
missiles; drones shutting Genoa airport; a tanker burning after a mine
strike east of the Strait of Hormuz; Cyclone Akvan making landfall in
Odisha; Trump putting any Iran decision off to 2027; Houthi missiles
targeting Riyadh. Every story happened, or was first reported, on
20 November 2026.

## How it works

- `compose.py` draws `entry.png` (1024×1024, Pillow) from scratch: cream
  newsprint, a black dateline band reading **20 NOVEMBER 2026**, one lead
  story and five panels, each with a simple original illustration.
- `main.py` (Python 3, standard library only) copies `entry.png` to
  `$MAKEFUN_OUTPUT_DIR/entry.png` (default `/output`), after validating
  the PNG gate limits (≤1024×1024 px, ≤1 MiB). Both runs write identical
  bytes.

## Run it

```sh
python3 compose.py          # regenerate entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Sources

Reuters (Kyiv, Hormuz oil, Trump/Iran), Al Jazeera (Hormuz mine strike),
India Meteorological Department / ANI (Cyclone Akvan), Corriere della Sera
via press reports (Genoa airport), Saudi-led coalition statements (Riyadh).
All artwork is original, drawn with Pillow; no photograph or third-party
artwork is used.
