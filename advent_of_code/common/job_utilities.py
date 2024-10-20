from datetime import datetime
from pathlib import Path

FIRST_AVAILABLE_YEAR = 2015
DEFAULT_SESSION_COOKIE_VALUE_PATH = Path.home() / ".advent-of-code-session-cookie-value"


def get_cookies(session_cookie_value_path: Path | None = None) -> dict[str, str]:
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
    if session_cookie_value_path is None:
        session_cookie_value_path = get_default_session_cookie_value_path()
    session_cookie_value = session_cookie_value_path.read_text()
    cookies = {"session": session_cookie_value}
    return cookies


def get_default_session_cookie_value_path() -> Path:
    return DEFAULT_SESSION_COOKIE_VALUE_PATH


def determine_first_aoc_available_year() -> int:
    return FIRST_AVAILABLE_YEAR


def determine_last_aoc_available_year() -> int:
    now = datetime.now()
    if now.month == 12:
        latest_available_year = now.year
    else:
        latest_available_year = now.year - 1
    return latest_available_year
