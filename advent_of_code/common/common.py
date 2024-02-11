import sys
import tomllib
from pathlib import Path
from typing import Any

import numpy as np
import numpy.typing as npt
import xarray as xr


def load_input_text_file_from_filename(filename: str) -> str:
    year, day = get_year_and_day_from_filename(filename)
    return load_puzzle_input_text_file(year, day)


def create_output_file_path_from_filename(
    output_filename: str, output_subdir: str, current_filename: str
) -> Path:
    year, day = get_year_and_day_from_filename(current_filename)
    return create_output_file_path(output_filename, output_subdir, year, day)


def get_year_and_day_from_filename(filename: str) -> tuple[int, int]:
    year, day = tuple(int(i) for i in Path(filename).stem.split("_") if i.isdigit())
    return year, day


def load_puzzle_input_text_file(year: int, day: int) -> str:
    input_path = get_input_file_path(year, day)
    assert input_path.is_file()
    text = input_path.read_text()
    return text


def get_input_file_path(year: int, day: int) -> Path:
    input_path = render_central_input_path(year, day)
    input_path = get_private_resources_path() / Path(input_path)
    return input_path


def get_private_resources_path() -> Path:
    return (Path.home() / Path("dev/advent-of-code-private")).resolve()


def get_example_inputs_file_contents() -> dict[str, dict[str, str]]:
    with get_example_inputs_file_path().open(mode="rb") as fp:
        contents = tomllib.load(fp)
    return contents


def get_example_inputs_file_path() -> Path:
    example_inputs_path = "resources/advent_of_code/example_inputs.toml"
    return get_private_resources_path() / example_inputs_path


def save_txt(text: str, filename: str, module_name: str, *, output_subdir: str = ""):
    output_file_path = create_output_file_path_from_filename(
        filename, output_subdir, module_name
    )

    output_file_path.write_text(text)

    print(f"Saved text to {output_file_path}")


def create_output_file_path(
    output_filename: str, output_subdir: str, year: int, day: int
) -> Path:
    output_dir_central = render_central_output_dir(year, day)
    output_dir_path = Path(output_dir_central) / output_subdir
    output_dir_path.mkdir(exist_ok=True, parents=True)
    output_file_path = output_dir_path / output_filename
    return output_file_path


def render_central_input_path(year: int, day: int):
    return (
        f"resources/advent_of_code/personalized_inputs/"
        f"year_{year}/input_year_{year}_day_{day:02d}.txt"
    )


def render_central_output_dir(year: int, day: int):
    return f"generated/advent_of_code/year_{year}/day_{day:02d}"


def adapt_recursion_limit(new_value: int = 15000, *, silent: bool = False):
    if not silent:
        print("Current recursion limit:")
    if not silent:
        print(sys.getrecursionlimit())

    sys.setrecursionlimit(new_value)

    if not silent:
        print("New recursion limit:")
    if not silent:
        print(sys.getrecursionlimit())


def render_2d_data_array(xda: xr.DataArray) -> str:
    return render_2d_numpy_array(xda.data)


def render_2d_numpy_array(data: npt.NDArray[np.uint8]) -> str:
    return "\n".join(line.tobytes().decode("utf-8") for line in data)


def parse_2d_string_array_to_uint8_xarray(text: str) -> xr.DataArray:
    input_array = parse_2d_string_array_to_uint8(text)
    return numpy_2d_to_xarray_row_col(input_array)


def numpy_2d_to_xarray_row_col(input_array: npt.NDArray[Any]):
    return xr.DataArray(
        input_array,
        coords={
            "row": list(range(input_array.shape[0])),
            "col": list(range(input_array.shape[1])),
        },
    )


def parse_2d_string_array_to_uint8(text: str) -> npt.NDArray[np.uint8]:
    lines = text.strip().split("\n")
    # Typing this expression seems impossible right now
    return lines_to_2d_uint8_array(lines)


def lines_to_2d_uint8_array(lines: list[str]) -> npt.NDArray[np.uint8]:
    return np.array([np.fromstring(line, dtype=np.uint8) for line in lines])  # type: ignore


def view_uint8_as_s1(array: npt.NDArray[np.uint8]) -> npt.NDArray[Any]:  # dtype='<U1'
    return array.view("S1")


def parse_2d_string_array_to_u1(text: str) -> npt.NDArray[Any]:  # dtype='<U1'
    lines = text.strip().split("\n")
    return np.array([np.array(list(line)) for line in lines])


def parse_2d_list_int_array(text: str) -> npt.NDArray[np.int32]:
    lines = text.strip().split("\n")
    # Typing this expression seems impossible right now
    return [np.fromstring(line, dtype=np.int32) for line in lines]  # type: ignore


def parse_2d_int_array(text: str) -> npt.NDArray[np.int32]:
    return np.array(parse_2d_list_int_array(text))
