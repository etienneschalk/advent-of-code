import sys
from pathlib import Path
from typing import Any

import numpy as np
import numpy.typing as npt
import xarray as xr


def load_input_text_file_from_filename(filename: str) -> str:
    year, day = get_year_and_day_from_filename(filename)
    text = load_puzzle_input_text_file(year, day)
    return text


def get_year_and_day_from_filename(filename: str) -> tuple[int, int]:
    year, day = tuple(int(i) for i in Path(filename).stem.split("_") if i.isdigit())
    return year, day


def load_puzzle_input_text_file(year: int, day: int) -> str:
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


def render_2d_numpy_array(data: npt.NDArray[np.uint8]) -> str:
    return "\n".join(line.tobytes().decode("utf-8") for line in data)


def parse_2d_string_array_to_uint8(text: str) -> npt.NDArray[np.uint8]:
    lines = text.strip().split("\n")
    # Typing this expression seems impossible right now
    return np.array([np.fromstring(line, dtype=np.uint8) for line in lines])  # type: ignore


def parse_2d_string_array_to_u1(text: str) -> npt.NDArray[Any]:  # dtype='<U1'
    lines = text.strip().split("\n")
    return np.array([np.array(list(line)) for line in lines])


def parse_2d_list_int_array(text: str) -> npt.NDArray[np.int32]:
    lines = text.strip().split("\n")
    # Typing this expression seems impossible right now
    return [np.fromstring(line, dtype=np.int32) for line in lines]  # type: ignore


def parse_2d_int_array(text: str) -> npt.NDArray[np.int32]:
    return np.array(parse_2d_list_int_array(text))
