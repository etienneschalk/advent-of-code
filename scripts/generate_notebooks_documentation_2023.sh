#!/bin/bash

cd docs

# Run non-interactively all notebooks for a glob path:
YEAR=2023
jupyter nbconvert --inplace --execute /home/tselano/dev/advent-of-code/docs/source/notebooks/$YEAR/notebook_problem_*.ipynb

poetry run sphinx-build source _build/html
