import sys
from pathlib import Path

import numpy as np
import xarray as xr


def load_input_text_file(filename: str) -> str:
    year, day = get_year_and_day_from_filename(filename)
    text = load_input_text(year, day)
    return text


def get_year_and_day_from_filename(filename: str) -> tuple[int, int]:
    return tuple(int(i) for i in Path(filename).stem.split("_") if i.isdigit())


def load_input_text(year: int, day: int) -> str:
    input_path = get_input_file_path(year, day)
    assert input_path.is_file()
    text = input_path.read_text()
    return text


def get_input_file_path(year: int, day: int) -> Path:
    input_path = (
        f"resources/advent_of_code/year_{year}/input_year_{year}_day_{day:02d}.txt"
    )
    input_path = Path(input_path)
    return input_path


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


def adapt_recursion_limit(new_value: int = 15000):
    print("Current recursion limit:")
    print(sys.getrecursionlimit())
    sys.setrecursionlimit(new_value)
    print("New recursion limit:")
    print(sys.getrecursionlimit())


def render_2d_data_array(xda: xr.DataArray) -> str:
    return render_2d_numpy_array(xda.data)


def render_2d_numpy_array(data: np.ndarray) -> str:
    return "\n".join(line.tobytes().decode("utf-8") for line in data)
