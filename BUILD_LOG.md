# BUILD_LOG — news-image-20261123

- Competition: "Sum up 23 November's world news in one image", $100 (top 50),
  deadline 2026-11-25T00:00:00Z (07:00 WIB 25 Nov 2026). Blind rounds; next round 2026-11-23T12:00:00Z.
- Kit: level 36 (0.1.0, build 98fe3e67b4f8). Output: /output/entry.png, PNG/JPEG, <=1 MiB, <=1024x1024.
- Suggested repo: `makefun-news-image-20261123` (owner verren044).
- Entry title: "The World in One Day — Monday 23 November 2026".

## Approach
Newspaper front page drawn fully in code with Pillow (no external images, no
network): black masthead "THE WORLD IN ONE DAY / MONDAY, 23 NOVEMBER 2026",
lead story (COP31 climate deal collapses as EU rejects a draft with no fossil
fuels), a world map with 10 numbered markers linked to the 10 biggest stories,
and a 6x5 grid of 30 short stories with category kicker, number, headline and
a minimal pictogram. Fonts (DejaVu) are bundled under fonts/ so rendering is
identical in the grader sandbox.

## Stories included (30, verified from web headlines for 23 Nov 2026)
1 COP31 deal collapses over fossil fuels (Antalya) · 2 Iran-US war widens to
Saudi, Bahrain · 3 14 missing after drone hits Kyiv flats · 4 Russian cargo
ship ablaze off Finland · 5 Lisbon march on living costs · 6 50 missing after
Indonesian factory fire · 7 Myanmar calls ASEAN ruling "unfair" · 8 Nepal PM
in Delhi for Modi talks · 9 South Korea minister quits over AI exam scandal ·
10 India record 720/9 in Wellington Test · 11 Poland: Russian missiles
crossed border · 12 UK-EU Brexit reset deal · 13 Xi-Trump-Putin historic
Shenzhen summit · 14 ICJ: Myanmar committed Rohingya genocide · 15 AI chips
diverted to China, probe finds · 16 Shah's Arunachal infra push · 17 IFFI
BRICS film roundtable · 18 BJP MP Wadkute dies in Delhi · 19 Anupama keeps
world snooker crown · 20 Russia summons Finnish envoy · 21 Houthi missile at
Saudi Arabia stopped · 22 Uranium stays in Iran, minister says · 23 Trump: no
worry over Iran regime change · 24 US to build nuclear plant in Saudi ·
25 Tanker attacks hit record high (Hormuz) · 26 Kashmir saffron fields used
as dump · 27 Hyderabad campus protests go on · 28 Nine pilgrims killed in
Kota crash · 29 Six held after Mumbai assault · 30 World chess title fight
goes on.

## Practice
- `MAKEFUN_OUTPUT_DIR=/tmp/nout1 python3 main.py` -> entry.png 121,901 bytes, 1024x1024 PNG.
- Second run byte-identical: sha256 49a1176eaa4f578b8e65197304f356c2a436056b01e70e8fd555fd31e05f9975 (both runs).
- Rendered image inspected visually: masthead, lead, map and all 30 tiles
  legible; fixed map overflow (land now clipped to map box), footer clipping,
  and two headline widows before final run.

## Notes for submitter
- Do NOT commit kit/. Repo must be created after the competition opens.
- Entry is main.py (Python 3.13, stdlib + Pillow, deterministic, no clock/network).
- Blind rounds: submit before 2026-11-23T12:00:00Z to enter round 2.
