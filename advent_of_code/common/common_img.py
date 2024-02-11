import numpy as np
import numpy.typing as npt
from PIL import Image

from advent_of_code.common.common import create_output_file_path_from_filename


def save_img(
    array: npt.NDArray[np.uint8] | npt.NDArray[np.bool_],
    filename: str,
    module_name: str,
    *,
    output_subdir: str = "",
):
    """Saves an image

    Parameters
    ----------
    array
        _description_
    filename
        _description_
    module_name
        _description_
    output_subdir, optional
        _description_, by default ""
    """
    output_file_path = create_output_file_path_from_filename(
        filename, output_subdir, module_name
    )

    im = Image.fromarray(array)
    im.save(output_file_path)

    print(f"Saved image to {output_file_path}")
