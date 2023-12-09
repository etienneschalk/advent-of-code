from advent_of_code.common import load_input_text_file

ProblemDataType = list[list[int]]


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    parsed_input = parse_input_text_file()
    result = compute_max_calories_part_1(parsed_input)
    return result


def compute_part_2():
    parsed_input = parse_input_text_file()
    result = compute_max_calories_part_2(parsed_input)
    return result


def compute_max_calories_part_1(parsed_input: ProblemDataType) -> int:
    return max(sum(group) for group in parsed_input)


def compute_max_calories_part_2(parsed_input: ProblemDataType, limit: int = 3) -> int:
    return sum(sorted((sum(group) for group in parsed_input), reverse=True)[:limit])


def parse_input_text_file() -> ProblemDataType:
    text = load_input_text_file(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> ProblemDataType:
    return [[int(n) for n in group.split("\n")] for group in text.strip().split("\n\n")]


if __name__ == "__main__":
    main()
