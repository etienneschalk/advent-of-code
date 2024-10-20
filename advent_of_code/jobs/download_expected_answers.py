import json
import re
from datetime import datetime
from pathlib import Path

import click
import requests

FIRST_AVAILABLE_YEAR = 2015
DEFAULT_SESSION_COOKIE_VALUE_PATH = Path.home() / ".advent-of-code-session-cookie-value"
DEFAULT_USERNAME = "eschalk"
DEFAULT_EXPECTED_ANSWERS_LOCATION = (
    Path.home()
    / "dev"
    / "advent-of-code-private"
    / "resources"
    / "advent_of_code"
    / "personalized"
    / DEFAULT_USERNAME
    / "expected_answers"
)


@click.command()
@click.option(
    "--year",
    type=int,
    help="Year, eg '2023'. If not provided, download for all available years",
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
    "--session_cookie_value_path",
    type=click.Path(path_type=Path),
    help="Root directory into which download the expected answers.",
    default=DEFAULT_SESSION_COOKIE_VALUE_PATH,
)
@click.option(
    "--dry_run",
    is_flag=True,
    show_default=True,
    default=False,
    help="Dry Run",
)
def download_expected_answers(
    year: int | None,
    day: int | None,
    expected_answers_location: Path,
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
        first_year = FIRST_AVAILABLE_YEAR
        last_year = determine_latest_available_year()
    else:
        # One turn of loop only for the desired year!
        first_year = last_year = year

    if day is None:
        first_day = 1
        last_day = 25
    else:
        # One turn of loop only for the desired day!
        first_day = last_day = day

    click.echo(
        f"Download years {first_year}-{last_year}, days {first_day}-{last_day} "
        f"into {expected_answers_location}"
    )
    click.echo(f"Using session cookie from {session_cookie_value_path}")

    if dry_run:
        click.echo("Quitting because dry run enabled.")

    download_expected_answers_internal(
        first_year,
        last_year,
        first_day,
        last_day,
        expected_answers_location,
        get_cookies(session_cookie_value_path),
    )


def download_expected_answers_internal(
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

        existing_year_expected_answers = json.loads(
            expected_answers_file_path.read_text()
        )
        existing_year_expected_answers.update(year_expected_answers)
        expected_answers_file_path.write_text(
            json.dumps(existing_year_expected_answers, indent=4, sort_keys=True)
        )
        click.echo(expected_answers_file_path)


def get_cookies(session_cookie_value_path: Path) -> dict[str, str]:
    """
    Get a cookies dict containing the session cookie.

    How to retrieve the cookies:
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    After having successfully logged in advent of code,
    get the cookie session value and store it in home.
    This cookie can later be used to retrieve authentication-protected
    data from the advent of code website, in an automated way.

    Parameters
    ----------
    session_cookie_value_path
        Path to a file containing the session, by default DEFAULT_SESSION_COOKIE_VALUE_PATH

    Returns
    -------
        Cookies dict to be passed to the requests.
    """
    session_cookie_value = session_cookie_value_path.read_text()
    cookies = {"session": session_cookie_value}
    return cookies


def determine_latest_available_year() -> int:
    now = datetime.now()
    if now.month == 12:
        latest_available_year = now.year
    else:
        latest_available_year = now.year - 1
    return latest_available_year


if __name__ == "__main__":
    download_expected_answers()  # type: ignore
