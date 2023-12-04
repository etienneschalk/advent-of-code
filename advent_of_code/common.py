from pathlib import Path


def load_input_text_file(filename: str) -> str:
    year, day = get_year_and_day_from_filename(filename)
    text = load_input_text(year, day)
    return text


def get_year_and_day_from_filename(filename: str) -> tuple[int, int]:
    return tuple(int(i) for i in Path(filename).stem.split("_") if i.isdigit())


def load_input_text(year: int, day: int) -> str:
    input_path = (
        f"resources/advent_of_code/year_{year}/input_year_{year}_day_{day:02d}.txt"
    )
    input_path = Path(input_path)
    assert input_path.is_file()
    text = input_path.read_text()
    return text
