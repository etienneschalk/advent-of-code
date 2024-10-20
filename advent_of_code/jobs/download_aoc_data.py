import json
import re
from pathlib import Path

import click
import requests

from advent_of_code.common.job_utilities import (
    DEFAULT_SESSION_COOKIE_VALUE_PATH,
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
ALL_CHOICES = [
    "expected_answers",
    "puzzle_inputs",
    "scores",
]
DEFAULT_USERNAME = "eschalk"
DEFAULT_PERSONALIZED_DATA_LOCATION = (
    Path.home()
    / "dev"
    / "advent-of-code-private"
    / "resources"
    / "advent_of_code"
    / "personalized"
    / DEFAULT_USERNAME
)
DEFAULT_EXPECTED_ANSWERS_LOCATION = (
    DEFAULT_PERSONALIZED_DATA_LOCATION / "expected_answers"
)
DEFAULT_PUZZLE_INPUTS_LOCATION = DEFAULT_PERSONALIZED_DATA_LOCATION / "puzzle_inputs"


@click.command()
@click.option(
    "--choices",
    help="Choices of mode of execution of the downloader tool.",
    type=click.Choice(ALL_CHOICES),
    required=True,
    multiple=True,
    # default=["scores"],
    default=ALL_CHOICES,
)
@click.option(
    "--year",
    type=int,
    help="Year, eg '2023'. If not provided, download for all available years.",
    default=None,
)
@click.option(
    "--day",
    type=int,
    help="Day, eg '9'. If not provided, download for all days 1-25.",
    default=None,
)
@click.option(
    "--expected_answers_location",
    type=click.Path(path_type=Path),
    help="Root directory into which download the expected answers.",
    default=DEFAULT_EXPECTED_ANSWERS_LOCATION,
)
@click.option(
    "--puzzle_inputs_location",
    type=click.Path(path_type=Path),
    help="Root directory into which download the puzzle inputs.",
    default=DEFAULT_PUZZLE_INPUTS_LOCATION,
)
@click.option(
    "--session_cookie_value_path",
    type=click.Path(path_type=Path),
    help="Location of the session value cookie file.",
    default=DEFAULT_SESSION_COOKIE_VALUE_PATH,
)
@click.option(
    "--dry_run",
    is_flag=True,
    show_default=True,
    default=False,
    help="Dry Run",
)
def download_aoc_data(
    choices: list[str],
    year: int | None,
    day: int | None,
    expected_answers_location: Path,
    puzzle_inputs_location: Path,
    session_cookie_value_path: Path,
    dry_run: bool,
):
    """Example usages:

    python advent_of_code/jobs/download_expected_answers.py

    python advent_of_code/jobs/download_expected_answers.py --dry_run

    python advent_of_code/jobs/download_expected_answers.py --year 2016 --day 9

    python advent_of_code/jobs/download_expected_answers.py --year 2016 --day 09

    """

    if year is None:
        first_year = determine_first_aoc_available_year()
        last_year = determine_last_aoc_available_year()
    else:
        # One turn of loop only for the desired year!
        first_year = last_year = year

    if day is None:
        first_day = 1
        last_day = 25
    else:
        # One turn of loop only for the desired day!
        first_day = last_day = day

    click.echo(f"Download years {first_year}-{last_year}, days {first_day}-{last_day}.")
    click.echo(f"Using session cookie from {session_cookie_value_path}")

    if dry_run:
        click.echo("Quitting because dry run enabled.")

    click.echo(f"Request: {choices=}")

    cookies = get_cookies(session_cookie_value_path)
    for choice in choices:
        if choice == "expected_answers":
            click.echo(
                f"[{choice}] "
                f"Download years {first_year}-{last_year}, days {first_day}-{last_day} "
                f"into {expected_answers_location}"
            )
            download_expected_answers(
                first_year,
                last_year,
                first_day,
                last_day,
                expected_answers_location,
                cookies,
            )
        elif choice == "puzzle_inputs":
            click.echo(
                f"[{choice}] "
                f"Download years {first_year}-{last_year}, days {first_day}-{last_day} "
                f"into {puzzle_inputs_location}"
            )
            download_puzzle_inputs(
                first_year,
                last_year,
                first_day,
                last_day,
                puzzle_inputs_location,
                cookies,
            )
        elif choice == "scores":
            download_scores(
                first_year,
                last_year,
                cookies,
            )
        else:
            click.echo(f"Illegal {choice=} (must be one of {ALL_CHOICES})", err=True)


def download_scores(
    first_year: int,
    last_year: int,
    cookies: dict[str, str],
):
    scores: dict[int, int] = {}
    for year in range(first_year, last_year + 1):
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


def download_expected_answers(
    first_year: int,
    last_year: int,
    first_day: int,
    last_day: int,
    expected_answers_location: Path,
    cookies: dict[str, str],
):
    for year in range(first_year, last_year + 1):
        expected_answers_file_path = (
            expected_answers_location / f"y_{year}" / f"expected_answers_{year}.json"
        )
        expected_answers_file_path.parent.mkdir(exist_ok=True, parents=True)
        year_expected_answers = {}
        for day in range(first_day, last_day + 1):
            result = requests.get(
                f"https://adventofcode.com/{year}/day/{day}", cookies=cookies
            )
            click.echo(f"{result.status_code}, {year}, {day}")
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
                click.echo(
                    f"Non-200 status code for {year=} {day=} ({result.status_code=})"
                )

        if expected_answers_file_path.is_file():
            existing_year_expected_answers = json.loads(
                expected_answers_file_path.read_text()
            )
            existing_year_expected_answers.update(year_expected_answers)
        else:
            existing_year_expected_answers = year_expected_answers
        expected_answers_file_path.write_text(
            json.dumps(existing_year_expected_answers, indent=4, sort_keys=True)
        )
        click.echo(expected_answers_file_path)


def download_puzzle_inputs(
    first_year: int,
    last_year: int,
    first_day: int,
    last_day: int,
    puzzle_inputs_location: Path,
    cookies: dict[str, str],
):
    for year in range(first_year, last_year + 1):
        for day in range(first_day, last_day + 1):
            puzzle_input_file_path = (
                puzzle_inputs_location
                / f"y_{year}"
                / f"puzzle_input_{year}{day:02d}.txt"
            )
            puzzle_input_file_path.parent.mkdir(exist_ok=True, parents=True)
            result = requests.get(
                f"https://adventofcode.com/{year}/day/{day}/input", cookies=cookies
            )
            print(result.status_code)
            if (result.status_code) == 200:
                puzzle_input_file_path.write_bytes(result.content)
                print(puzzle_input_file_path)
            else:
                print(f"Non-200 status code for {year=} {day=} ({result.status_code=})")


if __name__ == "__main__":
    download_aoc_data()  # type: ignore
