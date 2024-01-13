import numpy as np
import numpy.typing as npt
from PIL import Image

from advent_of_code.common import create_output_file_path


def save_img(
    array: npt.NDArray[np.uint8] | npt.NDArray[np.bool_],
    filename: str,
    module_name: str,
    *,
    output_subdir: str = "",
):
    output_file_path = create_output_file_path(filename, output_subdir, module_name)

    im = Image.fromarray(array)
    im.save(output_file_path)

    print(f"Saved image to {output_file_path}")
