import re

import requests

from advent_of_code.common.job_utilities import (
    determine_first_aoc_available_year,
    determine_last_aoc_available_year,
    get_cookies,
)

color_gradient_red_to_green_hex_26 = [
    "CB0E0E",  # Redish
    "C3140E",
    "BB1A0D",
    "B4200D",
    "AC270C",
    "A42D0C",
    "9C330B",
    "94390B",
    "8D3F0A",
    "85450A",
    "7D4C09",
    "755209",
    "6D5808",
    "665E08",
    "5E6407",
    "566A07",
    "4E7106",
    "467706",
    "3F7D05",
    "378305",
    "2F8904",
    "278F04",
    "1F9603",
    "189C03",
    "10A202",
    "08A802",  # Greenish
]

cookies = get_cookies()
scores: dict[int, int] = {}
for year in range(
    determine_first_aoc_available_year(), determine_last_aoc_available_year() + 1
):
    result = requests.get(f"https://adventofcode.com/{year}", cookies=cookies)
    print(result.status_code, year)
    if (result.status_code) == 200:
        _match = re.search(
            r'<span class="star-count">(\d+)\*</span>',
            result.content.decode("utf-8"),
        )
        score = 0 if _match is None else int(_match.group(1))
        scores[year] = score
    else:
        print(f"Non-200 status code for {year=} ({result.status_code=})")

print(scores)
print("-----")
for year, score in scores.items():
    badge_md_img = (
        f"![AOC {year}]"
        "(https://img.shields.io/badge/AOC%20"
        f"{year}-{score}%20%E2%AD%90-{color_gradient_red_to_green_hex_26[score//2]})"
    )
    print(badge_md_img)
