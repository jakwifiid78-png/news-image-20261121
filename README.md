# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/jakwifiid78-png/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/jakwifiid78-png/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

Entry for the make.fun competition **news-image-20261121** — "Sum up 21
November's world news in one image" ($100, top 50 paid).

`main.ts` (Node 22, standard library only) copies the committed
`entry.png` to `/output/entry.png`. The image is a 1024×1024 newspaper
front page — "THE WORLD — Saturday, 21 November 2026" — rendered
programmatically with Python + PIL (`gen.py`, deterministic: re-running
it produces byte-identical output).

## The day's news (all reported Saturday 21 November 2026)

1. **Wall Street in freefall** — S&P 500 −3.7% into correction,
   Nasdaq −5.3%, worst week in 18+ months; Nvidia −14%, AMD −13%.
   (Associated Press, Reuters)
2. **Russian missiles land in Poland** — two cruise missiles and a drone
   fall during NATO drills; the alliance calls it a violation.
   (Reuters, BBC)
3. **Trump, Xi and Putin meet** — first three-way summit in China ends;
   Trump defends calling Putin "a friend". (Reuters)
4. **South Africa mourns Mlambo-Ngcuka** — first woman deputy president
   and ex-UN Women chief dies aged 71. (Reuters)
5. **Shutdown looms over Iran war split** — Congress races to fund the
   government as Trump seeks $350bn more for defence. (Reuters)
6. **Trump: big tax on AI data centres abroad** — US firms building AI
   data centres overseas face a "tremendous tax". (Associated Press)

Sources in full: see [SOURCES.md](SOURCES.md).

## Run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```
