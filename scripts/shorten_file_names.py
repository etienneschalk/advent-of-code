import re
from pathlib import Path


def main():
    # Rename all filenames like "year_YYYY_day_DD" to "problem_YYYYDD"

    input_path = Path()

    for input_path in (Path(), Path().resolve().parent / "advent-of-code-private"):
        print(input_path)
        paths = sorted(
            (*input_path.rglob("*year_*day*.py"), *input_path.rglob("*year_*day*.txt"))
        )
        print(paths)
        for path in paths:
            result = re.search(r"year_(\d+)_day_(\d+)", path.stem)
            if result is None:
                continue
            year, day = result.group(1), result.group(2)
            print(year, day)
            new_stem = f"problem_{year}{day}"
            print(path.stem, "->", new_stem)
            path.resolve().rename(path.with_stem(new_stem).resolve())

            # Note for VSCode: Use search and replace with
            # Input regexp:
            # year_(\d+)_day_(\d+)
            # Output regexp:
            # problem_$1$2

    # Prefix test_ files
    tests_dir_path = Path("tests/advent_of_code")
    for path in sorted(tests_dir_path.rglob("problem_*.py")):
        path.resolve().rename(path.with_stem(f"test_{path.stem}").resolve())


if __name__ == "__main__":
    main()
