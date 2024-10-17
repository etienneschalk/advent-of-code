import json
import re
from pathlib import Path

import requests

first_year = 2015
latest_available_year = 2023

verbose = True
username = "eschalk"
expected_answers_location = (
    Path.home()
    / "dev"
    / "advent-of-code-private"
    / "resources"
    / "advent_of_code"
    / "personalized"
    / username
    / "expected_answers"
)

# After having successfully logged in advent of code,
# get the cookie session value and store it in home.
# This cookie can later be used to retrieve authentication-protected
# data from the advent of code website, in an automated way.
session_cookie_value_path = Path.home() / ".advent-of-code-session-cookie-value"
session_cookie_value = session_cookie_value_path.read_text()
cookies = {"session": session_cookie_value}

for year in range(first_year, latest_available_year + 1):
    expected_answers_file_path = (
        expected_answers_location / f"y_{year}" / f"expected_answers_{year}.json"
    )
    expected_answers_file_path.parent.mkdir(exist_ok=True, parents=True)
    year_expected_answers = {}
    for day in range(1, 25 + 1):
        result = requests.get(
            f"https://adventofcode.com/{year}/day/{day}", cookies=cookies
        )
        print(result.status_code, year, day)
        if (result.status_code) == 200:
            answers = re.findall(
                r"Your puzzle answer was <code>(.+?)</code>",
                result.content.decode("utf-8"),
            )
            # If all answers are numeric, consider the problem to have numeric solutions.
            if all(answer.isnumeric() for answer in answers):
                answers = list(map(int, answers))
            answers_dict = {k + 1: answers[k] for k in range(len(answers))}
            year_expected_answers[f"{year}{day:02d}"] = answers_dict
        else:
            print(f"Non-200 status code for {year=} {day=} ({result.status_code=})")
    expected_answers_file_path.write_text(json.dumps(year_expected_answers, indent=4))
    print(expected_answers_file_path)
