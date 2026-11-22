# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/DarelHarteraVBY2C/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/DarelHarteraVBY2C/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A one-page newspaper front page summing up world news for Saturday, 21 November 2026. Built for the [make.fun news-image-20261121 bounty](https://make.fun/bounty/news-image-20261121) ("Sum up 21 November's world news in one image", $100 in USDC).

## The front page

The lead story is Russia's biggest strike of the year on Kyiv. The other stories on the page:

- **Wall Street in correction** as AI stocks crash: S&P -3.7%, Nasdaq -5.28%.
- **Trump presses Europe on Ukraine** spending.
- **Mexico captures "El Chapo Isidro"**, an FBI Top-10 fugitive, in Sinaloa.
- **COP31 spills into overtime** over fossil fuels.

A strip along the bottom covers Anthropic's slide to $88.90, two tankers hit in the Strait of Hormuz, and the UK-EU youth mobility deal.

## How it works

`compose.py` lays out the five generated photo panels and the day's headlines into `entry.jpg` (1024×1024, under 1 MiB). `main.ts` validates that image and copies it to the output directory as `entry.png`.

```sh
python3 compose.py
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

Running `main.ts` twice writes byte-identical output.

## License

MIT. See `LICENSE`.
