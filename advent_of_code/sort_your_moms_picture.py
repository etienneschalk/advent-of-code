import shutil
from collections import defaultdict
from pathlib import Path

from PIL import Image

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# BEFORE RUNNING THIS SCRIPT MAKE A BACKUP OF YOUR WHATSAPP PICTURES
# I AM NOT RESPONSIBLE FOR ANY DATA LOSS
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def main():
    dir_path = None  # changeme
    dir_path = Path(dir_path)

    # First pass: Identify dates
    img_paths = sorted(
        path for path in dir_path.glob("IMG-*-WA*") if path.suffix in {".jpg", ".jpeg"}
    )
    print(f"There are [{len(img_paths)}] received pictures (shallow).")

    # IMG-20190815-WA0001.jpg
    classified_by_year_month = get_classified_paths(img_paths)

    pictures_per_month = get_pictures_count(classified_by_year_month)
    print(pictures_per_month)

    for year_month_key, paths in classified_by_year_month.items():
        target_dir = dir_path / "sorted" / year_month_key
        target_dir.mkdir(parents=True, exist_ok=True)
        for source_path in paths:
            target_path = target_dir / source_path.name
            print(f"{source_path}")
            print(f"{target_path}")
            if target_path.exists():
                print(f"{target_path=} already exists, exiting immediately.")
                exit(-1)
            source_path.rename(target_path)

    sorted_dir = dir_path / "sorted"
    keys = sorted(x for x in sorted_dir.iterdir() if x.is_dir())
    year_month_to_paths = {
        key.name: sorted((sorted_dir / key).glob("*")) for key in keys
    }
    potential_collages = []
    for year_month_key, paths in year_month_to_paths.items():
        print(f"In {year_month_key}, There are {len(paths)} pictures to look up.")
        for path in paths:
            with Image.open(path) as image_file:
                width, height = image_file.size
                print(f"    ... Analyzing {path=} ; {width=}, {height=}")
                if image_file.size == (2048, 2048) or image_file.size == (1448, 1448):
                    print("    ! Found collage")
                    potential_collages.append(path)

    print(f"{potential_collages=}")
    print(f"{len(potential_collages)} potential collages")
    classified_collages_by_year_month = get_classified_paths(potential_collages)
    print(classified_collages_by_year_month)
    classified_collages_by_year_month_count = get_pictures_count(
        classified_collages_by_year_month
    )
    print(classified_collages_by_year_month_count)
    ...

    for year_month_key, paths in classified_collages_by_year_month.items():
        flatten = True
        target_dir = dir_path / "sorted_collages"
        if flatten:
            target_dir = target_dir / "flatten"
        else:
            target_dir = target_dir / year_month_key
        target_dir.mkdir(parents=True, exist_ok=True)
        for source_path in paths:
            target_path = target_dir / source_path.name
            print(f"{source_path}")
            print(f"{target_path}")
            if target_path.exists():
                print(f"{target_path=} already exists, exiting immediately.")
                exit(-1)
            shutil.copy(source_path, target_path)


def get_pictures_count(classified_by_year_month):
    return {k: len(v) for k, v in classified_by_year_month.items()}


def get_classified_paths(img_paths):
    classified_by_year_month = defaultdict(list)
    for path in img_paths:
        classified_by_year_month[get_month_from_img_filename(path)].append(path)
    return classified_by_year_month


def get_month_from_img_filename(path: Path) -> str:
    return path.stem[4 : 4 + 6]


if __name__ == "__main__":
    main()
