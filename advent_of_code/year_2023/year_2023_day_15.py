import numpy as np

from advent_of_code.common import load_input_text_file

ProblemDataType = list[str]


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    data = parse_input_text_file()
    result = compute_total_load(data)
    return result


def compute_part_2():
    data = parse_input_text_file()
    return None


def compute_total_load(parsed_input: ProblemDataType):
    split = [line.split("#") for line in parsed_input]
    cube_rock_idx = tuple(
        tuple((*(idx for idx, c in enumerate(li) if c == "#"), len(li)))
        for li in parsed_input
    )
    round_rock_count = tuple(
        tuple(sum(el == "O" for el in li) for li in line) for line in split
    )
    loads = [
        list(some_math(x, y) for x, y in zip(a, b))
        for a, b in zip(cube_rock_idx, round_rock_count)
    ]
    return sum(sum(x) for x in loads)


def some_math(goal: int, length: int) -> int:
    go = goal
    le = length
    return ((go * (go + 1)) - ((go - le) * (go - le + 1))) // 2


def parse_input_text_file() -> ProblemDataType:
    text = load_input_text_file(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> ProblemDataType:
    lines = text.strip().split("\n")
    input_array = np.array([np.fromstring(line, dtype="<S1") for line in lines])
    tolist = input_array.T.tolist()
    data = ["".join(i.decode() for i in reversed(li)) for li in tolist]
    return data


if __name__ == "__main__":
    main()
