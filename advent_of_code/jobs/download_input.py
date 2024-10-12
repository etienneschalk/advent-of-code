from pathlib import Path

import requests

latest_available_year = 2023

verbose = False
username = "eschalk"
puzzle_inputs_location = (
    Path.home()
    / "dev"
    / "advent-of-code-private"
    / "resources"
    / "advent_of_code"
    / "personalized"
    / username
    / "puzzle_inputs"
)

# After having successfully logged in advent of code,
# get the cookie session value and store it in home.
# This cookie can later be used to retrieve authentication-protected
# data from the advent of code website, in an automated way.
session_cookie_value_path = Path.home() / ".advent-of-code-session-cookie-value"
session_cookie_value = session_cookie_value_path.read_text()
cookies = {"session": session_cookie_value}

for year in range(2015, latest_available_year + 1):
    for day in range(1, 25 + 1):
        puzzle_input_file_path = (
            puzzle_inputs_location / f"y_{year}" / f"puzzle_input_{year}{day:02d}.txt"
        )
        puzzle_input_file_path.parent.mkdir(exist_ok=True, parents=True)
        result = requests.get(
            f"https://adventofcode.com/{year}/day/{day}/input", cookies=cookies
        )
        print(result.status_code)
        if (result.status_code) == 200:
            if verbose:
                print(result.content)
            puzzle_input_file_path.write_bytes(result.content)
            print(puzzle_input_file_path)
        else:
            print(f"Non-200 status code for {year=} {day=} ({result.status_code=})")
