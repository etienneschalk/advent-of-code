#!/bin/bash

INPUT_PNG_DIR=$HOME/dev/advent-of-code/generated/advent_of_code/year_2023/day_10/mazegen
OUTPUT_VID=$HOME/dev/advent-of-code/generated/advent_of_code/year_2023/day_10
cd "${INPUT_PNG_DIR}"

ffmpeg \
    -framerate 5800 \
    -pattern_type glob -i '*.png' \
    -c:v libx264 \
    -pix_fmt yuv420p "${OUTPUT_VID}/out.mp4"

cd -
