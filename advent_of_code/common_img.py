import numpy as np
from PIL import Image

from advent_of_code.common import create_output_file_path


def save_img(
    array: np.ndarray, filename: str, module_name: str, *, output_subdir: str = ""
):
    output_file_path = create_output_file_path(filename, output_subdir, module_name)

    im = Image.fromarray(array)
    im.save(output_file_path)

    print(f"Saved image to {output_file_path}")
