# advent-of-code

## Table of Contents

- [advent-of-code](#advent-of-code)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Terminology](#terminology)
  - [Documentation](#documentation)
    - [Deploy on GitHub Pages](#deploy-on-github-pages)
    - [Local](#local)
    - [Misc](#misc)
      - [About pre-running the Notebooks](#about-pre-running-the-notebooks)
      - [Convert SVGs to PNGs](#convert-svgs-to-pngs)
    - [Miscellaneous](#miscellaneous)
  - [Installation](#installation)
    - [Sources](#sources)
      - [From GitHub](#from-github)
    - [Resources](#resources)
      - [From GitHub](#from-github-1)
        - [How-to: Obliterate private files from GitHub history](#how-to-obliterate-private-files-from-github-history)
      - [Create your own Test Data](#create-your-own-test-data)
  - [Development](#development)
    - [Testing](#testing)
      - [pytest](#pytest)
    - [Code quality](#code-quality)
      - [pre-commit](#pre-commit)
    - [Troubleshooting](#troubleshooting)
      - [Revert the y-axis when plotting a (row-col) DataArray with matplotlib](#revert-the-y-axis-when-plotting-a-row-col-dataarray-with-matplotlib)
    - [(Legacy) Template Files](#legacy-template-files)

<!-- start include sphinx -->

## Introduction

[Information about Advent of Code](https://adventofcode.com/2023/about)

🚧 This section is work in progress

<!-- TODO eschalk differentiate technical and non-technical sections with emojis

🧑‍💼 Non-technical
🧑‍💻 Technical -->

## Terminology

[Advent of Code](https://adventofcode.com/about)
: Yearly coding challenge occurring in December

Puzzle (or _Problem_)
: A puzzle is defined by its year and day. It contains a Puzzle Description, and an associated

Puzzle Description
: The description associated to a Puzzle. It contains Puzzle Examples

Puzzle Example
: Any fenced raw text content in the Puzzle Description. Visually, it has a different background that the rest of the Puzzle Description. Include Example Puzzle Inputs

Solution
: An algorithm that takes as an input the Puzzle Input and produces as an output the associated answer.

Puzzle Input
: Raw text contents that the Solution takes as an input. The Solution is correct if its output is the Answer.

Personalized Puzzle Input
: Each user logged on the Advent of Code website gets a personalized Puzzle Input and a Personalized Answer. This is done to prevent copy pasting others' Answers, and also prevents the Advent of Code's website content to be stole and reproduced by third parties.

Example Puzzle Input
: One of the examples in the problem description. This is a sub-category of Puzzle Examples.

Answer
: A number or a string solving the associated Puzzle Input

Personalized Expected Answer
: Each user logged on the Advent of Code website gets a personalized Puzzle Input and a Personalized Answer. This is done to prevent copy pasting others' Answers, and also prevents the Advent of Code's website content to be stole and reproduced by third parties.

Data Model TODO eschalk

<!-- ```mermaid

``` -->

## Documentation

This documentation also fulfills the role of being a blog to share my solutions and visualizations.

### Deploy on GitHub Pages

Current issues with GitHub Actions:

- How to correctly install dependencies with poetry in the context of GitHub Actions, and make them available in the notebook runner when building the Sphinx documentation?
- How to access the private resources (personalized puzzle inputs, etc.)

No current solution for now. The issue is "how to make a GitHub action access private data"
https://docs.github.com/en/actions/creating-actions/sharing-actions-and-workflows-from-your-private-repository

A hack: Pre-run the notebook locally so that nbsphinx does not attempt to run it.
This remove the need of the notebook execution by the GitHub Action, and the problem of accessing the private resources.
However it means versioning the notebooks' outputs.
https://nbsphinx.readthedocs.io/en/0.5.0/pre-executed.html#Long-Running-Cells

### Local

````{note}
The documentation's dependencies are included in the `docs` dependency group of poetry in `pyproject.toml`

```bash
poetry install --with docs
```
````

```bash
cd docs

poetry run sphinx-build source _build/html
poetry run sphinx-build -E source _build/html # clear cache with -E

poetry run sphinx-autobuild source _build/html # autobuild (useful in development)
poetry run sphinx-autobuild -E source _build/html # clear cache (not advised with autobuild)

poetry run sphinx-serve -h 127.0.0.1 -p 8080 # just serve
```

Commonly used to test the doc before a deployment on GitHub Pages:

```bash
cd docs
poetry run sphinx-build -E source _build/html # clear cache with -E
poetry run sphinx-serve -h 127.0.0.1 -p 8080 # just serve
```

### Misc

#### About pre-running the Notebooks

Clear non-interactively all notebooks for a glob path:

```bash
YEAR=2023
jupyter nbconvert --inplace --clear-output /home/tselano/dev/advent-of-code/docs/source/notebooks/$YEAR/notebook_problem_*.ipynb
```

Run non-interactively all notebooks for a glob path:

```bash
YEAR=2023
jupyter nbconvert --inplace --execute /home/tselano/dev/advent-of-code/docs/source/notebooks/$YEAR/notebook_problem_*.ipynb
```

#### Convert SVGs to PNGs

If not installed, install inkscape

```bash
apt install inkscape
```

Run inkscape on all PNG files contained in a directory

```bash
for filename in docs/source/_static/img/thumbnails/*.svg; do inkscape -h 1024 $filename --export-png "${filename:0:-4}.png" --export-background black; done
```

Note: the `--export-background black` replaces the default transparent background by a black background. As dark-mode are the majority among plots, this is a safety net to avoid unreadables plots on a white background.

### Miscellaneous

Keep sidebar constant:
https://stackoverflow.com/questions/74075617/side-bar-navigation-incomplete-in-sphinx

Unwrap type aliases: wait for:
https://github.com/readthedocs/sphinx-autoapi/issues/414#issuecomment-1951389780

## Installation

### Sources

#### From GitHub

Repository can be found on GitHub: https://github.com/etienneschalk/advent-of-code

### Resources

#### From GitHub

In an effort not to share any personalized puzzle input nor personalized answer, as well as not reproducing the public example puzzle inputs, this data is not stored publicly in GitHub.

I previously stored. If it happens to you, you can read the following procedure to remove all traces of personalizes inputs in your git repository.

##### How-to: Obliterate private files from GitHub history

- Consult the following GitHub documentation page: [Removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)
- Download BFG from https://rtyley.github.io/bfg-repo-cleaner/
- Identifying the pattern of my personalized input filenames as I did store them: `"input_year_*.txt`
- Run the tool: `java -jar ~/bfg-1.14.0.jar --delete-files "input_year_*.txt"`
- Check the contents of `deleted-files.txt` in the tool's report to verify that all files of interest were removed.
- The tool indicated to run the following command: `BFG run is complete! When ready, run: git reflog expire --expire=now --all && git gc --prune=now --aggressive`
- `git push --force`
- Verify that the files were indeed obliterated from history
  - In my case, I checked a link to an old commit on GitHub. In fact, the files were still accessible but with a new admonition: `This commit does not belong to any branch on this repository, and may belong to a fork outside of the repository.`.
  - The offending files are _de facto_ not publicly anymore as one may need the old commit's hash to access it. One cannot just use the regular way of checking the git history in the GitHub UI anymore to access easily the removed files.
  - Maybe these orphan commits will be somehow garbage collected, but with a delay?

````{note}
Here is what the contents of `deleted-files.txt` in the BFG report looks like in my cas (only filenames):

```text
input_year_2022_day_01.txt
input_year_2022_day_02.txt
input_year_2022_day_03.txt
input_year_2022_day_04.txt
input_year_2022_day_05.txt
input_year_2022_day_24.txt
input_year_2022_day_25.txt
input_year_2023_day_00.txt
input_year_2023_day_01.txt
input_year_2023_day_02.txt
input_year_2023_day_03.txt
input_year_2023_day_04.txt
input_year_2023_day_05.txt
input_year_2023_day_06.txt
input_year_2023_day_07.txt
input_year_2023_day_08.txt
input_year_2023_day_08.txt
input_year_2023_day_09.txt
input_year_2023_day_09.txt
input_year_2023_day_1.txt
input_year_2023_day_10.txt
input_year_2023_day_11.txt
input_year_2023_day_12.txt
input_year_2023_day_13.txt
input_year_2023_day_14.txt
input_year_2023_day_15.txt
input_year_2023_day_15.txt
input_year_2023_day_16.txt
input_year_2023_day_17.txt
input_year_2023_day_18.txt
input_year_2023_day_19.txt
input_year_2023_day_2.txt
input_year_2023_day_20.txt
input_year_2023_day_21.txt
input_year_2023_day_22.txt
input_year_2023_day_23.txt
input_year_2023_day_24.txt
input_year_2023_day_25.txt
input_year_2023_day_3.txt
input_year_2023_day_4.txt
```
````

#### Create your own Test Data

You can create a configuration file that points to a folder. The following is a "well-known structure", using "convention over configuration" principle:

```text
${path_to_directory_with_private_resources}
└── resources
    └── advent_of_code
        ├── personalized
        │   └── ${username}
        │       ├── expected_answers
        │       │   └──  y_${year}
        │       │        └── (1) expected_answers_${year}.json
        │       └── puzzle_inputs
        │           └──  y_${year}
        │                └── (+) puzzle_input_${year}${day}.txt
        └── common
            └── example_puzzle_inputs
                └──  y_${year}
                     └── (1) example_inputs_${year}.toml
```

However, each file name is unique, and the resources reader internally use `rglob` with the expected filename, hence making the directory hierarchy irrelevant. I still respect this structure in my private resources, in the case that `rglob` would need to be replaced if it hampers too much the performance of the testing. For now, this has not happened.

It means only the filename convention is enforced, not the directory hierarchy.

1. Configuration file to point to `${path_to_directory_with_private_resources}`
2. Puzzle Inputs are the raw content you can get from problem description, without any further addition.
3. Expected Answers are to be completed by yourself once you solve the problem, for future reproducibility of your solutions

_Example_:

```json
{
  "202325": {
    "1": 11111111111,
    "2": "Part 2 of Day 25 is having solved all the 49 previous problems!"
  }
}
```

4. Example Puzzle Inputs are scrapped from the problem description. It is done manually as they are largely problem-specific

```{note}
This would be a nice addition to have an interface that automatically extracts all of the raw contents to such a folder, privately, and that generates this structure automatically.

This would be like this: Logged in AoC -> Download to well-known resources directory thanks to the scrapper and an auth token  -> Complete the resource folder once -> Usable by the solutions.

The well-know format could be language-independent.

Note: the expected answers would still need to be filled manually.
```

## Development

### Testing

#### pytest

TODO eschalk include pytest to pre-commit (ut, it, and slow)

````{note}
pytest is included in the `dev` dependency group of poetry in `pyproject.toml`

```bash
poetry install --with dev
```
````

Integration tests:

```bash
pytest --with-integration -k integration --durations=0
```

All tests : unit + integration tests. **Slow tests are excluded.**

```bash
poetry run pytest -v --with-integration --durations=0
```

**Only slow tests**, using multiple workers (requires `pytest-xdist`).

```bash
poetry run pytest -v --with-integration -m slow --durations=0 -n 4
```

Drawback: duration is displayed globally per worker, not for each individual test

Note: durations < 0.005 seem to be hidden. Use `-vv` to truly get all

```bash
poetry run pytest -vv --with-integration -m slow --durations=0 -n 4
```

See [Stack Overflow - Show durations of tests for pytest](https://stackoverflow.com/questions/27884404/printing-test-execution-times-and-pinning-down-slow-tests-with-py-test)

```bash
pytest --durations=0   # Show all times for tests and setup and teardown
pytest --durations=1   # Slowest test
pytest --durations=50  # Slowest 50 tests
```

### Code quality

#### pre-commit

````{note}
pre-commit is included in the `dev` dependency group of poetry in `pyproject.toml`

```bash
poetry install --with dev
```
````

Code quality is managed by [pre-commit](https://pre-commit.com/). This wonderful tool can be seen as a _local CI (continuous integration)_.

It runs all the useful tools improving the overall quality of a codebase. Here is a non-exhaustive list below (consult `.pre-commit-config.yaml` for more details):

- [autoflake](https://pypi.org/project/autoflake/): _autoflake removes unused imports and unused variables from Python code_
- [isort](https://pycqa.github.io/isort/): _isort is a Python utility / library to sort imports alphabetically, and automatically separated into sections and by type_
- [blackdoc](https://blackdoc.readthedocs.io/en/latest/): _apply black to code in documentation_
- [ruff](https://github.com/astral-sh/ruff): An extremely fast Python linter and code formatter, written in Rust.
- [pyright](https://github.com/microsoft/pyright): _Static Type Checker for Python_

It runs every time a commit is attempted, on the set of relevant files according to the diff.

There is a way to disable it (use with parcimony, bypassing today equals technical debt for tomorrow) with the `--no-verify` git flag. Example:

```bash
git commit -m "bypass pre-commit" --no-verify
```

To run all checks on the whole project:

```bash
pre-commit run --all
```

Run it on all the codebase, with the "manual" hook (for long operations that you don't want to have to wait for on every commit, like slow integration tests):

```bash
pre-commit run --all --hook-stage manual
```

TODO eschalk as pytest is not yet included, nor integration tests.

### Troubleshooting

#### Revert the y-axis when plotting a (row-col) DataArray with matplotlib

Use [`yincrease=False`](https://docs.xarray.dev/en/stable/generated/xarray.plot.imshow.html)

```python
mapping_xda.plot(y="row", x="col", col="pipe", yincrease=False)
```

Example in notebook_problem_202310

### (Legacy) Template Files

TODO -> Adapt the templating

Start development for a given day and year by generating template files:

```bash
python advent_of_code/jobs/code_generation.py --year 2022 --day 5
```

```text
Started Generation
Generating puzzle_input
    Written puzzle_input to resources/advent_of_code/year_2022/input_problem_202205.txt
Generating source_code
    Written source_code to advent_of_code/year_2022/problem_202205.py
Generating test_code
    Written test_code to tests/advent_of_code/year_2022/test_problem_202205.py
Finished Generation
```

<!-- end include sphinx -->
