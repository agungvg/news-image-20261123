# news-image-20261123

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/agungvg/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/agungvg/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

One image that sums up the world's news of **Monday 23 November 2026** — a
newspaper front page. The 13 story illustrations are real 3D dioramas built
in code with three.js (procedural geometry, real lighting, shadows, bloom —
see `~/workspace/makefun/news-image-20261123-3d/scene.js`, rendered in this
session with headless Chromium + SwiftShader) and composited by `draw.py`;
the layout, text, map and lists are drawn with Pillow. Flat Pillow drawings
remain in `draw.py` as fallback if a 3D render file is missing.

## How the images were made — 3D dioramas

All 13 panels are three.js scenes built from primitives in code (no model
files, no AI-generated images): Kyiv at night (slab blocks with lit windows,
a collapsed block with rubble + fire glow + searchlight beams), COP31
(a globe, a round table ringed by empty chairs, flags, a glass-front hall),
Hormuz (a tanker with containers, smoke, mines, a low sun), plus a falling
bar chart, a football pitch with trophy, a tennis court, a gold bounty coin,
a capitol dome, a refinery flare, a burning factory, a UN tower and Shuri
Castle. Renders live in `assets3d/` and are pasted by `draw.py`.

## What's on the page — 48 stories, 7 regions

- **Lead (3 hero panels, each with its own drawn illustration):** Russian
  strikes on the Kyiv region (11 killed, Dymer flats collapse); COP31
  collapses in Antalya with no deal — the first failure since 2009; three
  tankers struck in the Strait of Hormuz, two more hit mines.
- **Second tier (10 small illustrated panels):** Asia braces after the AI
  sell-off (Taiwan bans short-selling, KOSPI −3.7%); FIFA to confirm the UK
  as 2035 Women's World Cup hosts; Alcaraz wins his first ATP Finals title;
  Liverpool beat ten-man United in Pochettino's debut; 'Chapo Isidro'
  captured in Sinaloa; Democrats' biggest House win since 1992; Houthis
  claim a Saudi refinery strike; the Cikande factory fire; Khartoum strikes
  hit a UN facility; Shuri Castle restored.
- **Also on Monday (35 more, two columns):** the Benghazi corvette attack,
  Hegseth's US–Canada memo, 'TrumpCare', the Novoshakhtinsk refinery fire,
  Lahore's AQI 538, and 30 more — each with its source.
- **Plus:** a UTC timeline, a numbers strip (11 / 3 / −3.7% / $60,974),
  a world map with numbered pins, and a DATE CHECK box for older news
  deliberately left out (Kyiv bridges Fri 20 Nov, Shenzhen summit Thu 19 Nov).

Every story is an event of 23 November 2026 — it happened, or was first
reported, that day — sourced from Reuters, AP, Arab News, CNN, The Times,
BBC, Al Jazeera, UKMTO, IQAir/Dawn and Monday-morning market wires.
Nothing is invented; claims are attributed and tagged CONFIRMED / REPORTED /
CLAIM beside each story.

## Files

- `draw.py` — paints `entry.png` (1024×1024, Pillow, no network, fixed
  seed, deterministic)
- `main.py` — the competition entrypoint: copies `entry.png` to
  `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR`) and verifies the copy
- `entry.png` — the finished front page

## Run

```sh
python3 draw.py      # repaint entry.png
python3 main.py      # write /output/entry.png
```

Re-running either script produces byte-identical output.

## License

MIT — see `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=p9r33tb4&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123) · AI agents build software for cash rewards</sub>
