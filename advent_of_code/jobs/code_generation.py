from pathlib import Path
import click


@click.command()
@click.option(
    "--year",
    type=int,
    help="Year, eg '2023'",
)
@click.option(
    "--day",
    type=int,
    help="Day, eg '9'",
)
@click.option(
    "--dry_run",
    is_flag=True,
    show_default=True,
    default=False,
    help="Dry Run",
)
def code_generation_entrypoint(year: int, day: int, dry_run: bool):
    create_files_for_year_and_day_from_templates(year, day, dry_run)


def create_files_for_year_and_day_from_templates(
    year: int, day: int, dry_run: bool
) -> None:
    project_name = "advent_of_code"
    year_repr = f"year_{year}"
    day_repr = f"day_{day:02d}"
    source_code_template = render_source_code_template()
    test_code_template = render_test_code_template(year_repr, day_repr)

    template_to_path = {
        "puzzle_input": {
            "template": "",
            "target_path": f"resources/{project_name}/{year_repr}/input_{year_repr}_{day_repr}.txt",
        },
        "source_code": {
            "template": source_code_template,
            "target_path": f"{project_name}/{year_repr}/{year_repr}_{day_repr}.py",
        },
        "test_code": {
            "template": test_code_template,
            "target_path": f"tests/{project_name}/{year_repr}/test_{year_repr}_{day_repr}.py",
        },
    }

    for key, item in template_to_path.items():
        click.secho(f"Generating {key}", bg="green", fg="red", bold=True)
        template = item["template"]
        target_path = Path(item["target_path"])
        if target_path.exists():
            click.secho(
                f"    Skipped {target_path} because it exists",
                bg="green",
                fg="red",
                bold=True,
            )
            continue

        if not dry_run:
            (target_path).write_text(template)
            if not target_path.is_file():
                click.secho(
                    f"    Failed to write {target_path}",
                    bg="green",
                    fg="red",
                    bold=True,
                )

        click.secho(
            f"    Written {key} to {target_path}", bg="green", fg="red", bold=True
        )

    click.secho("Finished Generation", bg="green", fg="red", bold=True)


def render_test_code_template(year_repr: str, day_repr: str) -> str:
    test_code_template = rf"""
from advent_of_code.{year_repr}.{year_repr}_{day_repr} import parse_text_input

EXAMPLE_INPUT = '''

REPLACE_BY_EXAMPLE_INPUT_FROM_PROBLEM_DESCRIPTION

'''


def test_{year_repr}_{day_repr}_part_1():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)


def test_{year_repr}_{day_repr}_part_2():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)
"""

    return test_code_template


def render_source_code_template() -> str:
    source_code_template = rf"""
from advent_of_code.common import load_input_text_file

ProblemDataType = ...


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({{1: result_part_1, 2: result_part_2}})


def compute_part_1():
    data = parse_input_text_file()
    ...
    return None


def compute_part_2():
    data = parse_input_text_file()
    ...
    return None


def parse_input_text_file() -> ProblemDataType:
    text = load_input_text_file(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> ProblemDataType:
    lines = text.strip().split("\n")
    ...
    return lines


if __name__ == "__main__":
    main()
"""

    return source_code_template


if __name__ == "__main__":
    code_generation_entrypoint()
