from advent_of_code.common import load_input_text_file_from_filename

type ProblemDataType = tuple[tuple[str, str], ...]


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    data = parse_input_text_file()
    scores = compute_scores_for_part_1(data)
    result = sum(scores)
    return result


def compute_part_2():
    data = parse_input_text_file()
    scores = compute_scores_for_part_2(data)
    result = sum(scores)
    return result


def compute_scores_for_part_1(parsed_input: ProblemDataType):
    opponent_mapping = dict(zip("ABC", range(len("ABC"))))
    my_mapping = dict(zip("XYZ", range(len("XYZ"))))
    int_pairs = tuple((opponent_mapping[p[0]], my_mapping[p[1]]) for p in parsed_input)
    scores = compute_scores(int_pairs)
    return scores


def compute_scores_for_part_2(parsed_input: ProblemDataType):
    opponent_mapping = dict(zip("ABC", range(len("ABC"))))
    my_mapping = dict(zip("XYZ", (-1, 0, 1)))
    int_pairs = tuple(
        (opponent_mapping[p[0]], (opponent_mapping[p[0]] + my_mapping[p[1]]) % 3)
        for p in parsed_input
    )
    scores = compute_scores(int_pairs)
    return scores


def compute_scores(int_pairs: tuple[tuple[int, int], ...]) -> tuple[int, ...]:
    scores = tuple(3 * ((p[1] - p[0] + 1) % 3) + p[1] + 1 for p in int_pairs)
    return scores


def parse_input_text_file() -> ProblemDataType:
    text = load_input_text_file_from_filename(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> ProblemDataType:
    return tuple(
        (line.split()[0], line.split()[1]) for line in text.strip().split("\n")
    )


if __name__ == "__main__":
    main()
