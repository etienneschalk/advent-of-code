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


def save_txt(text: str, filename: str, module_name: str, *, output_subdir: str = ""):
    output_file_path = create_output_file_path(filename, output_subdir, module_name)

    output_file_path.write_text(text)

    print(f"Saved text to {output_file_path}")


def create_output_file_path(filename: str, output_subdir: str, current_filename: str):
    year, day = get_year_and_day_from_filename(current_filename)
    output_dir_central = f"generated/advent_of_code/year_{year}/day_{day:02d}"
    output_dir = Path(output_dir_central) / output_subdir
    output_dir.mkdir(exist_ok=True, parents=True)
    output_file_path = output_dir / filename
    return output_file_path
