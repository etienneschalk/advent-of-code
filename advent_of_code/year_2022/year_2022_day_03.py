from advent_of_code.common import load_input_text_file

ProblemDataType = tuple[tuple[str, str], ...]


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    parsed_input = parse_input_text_file()
    shared_items = find_shared_items_for_part_1(parsed_input)
    priority_sum = compute_priority_sum(shared_items)
    return priority_sum


def compute_part_2():
    parsed_input = parse_input_text_file()
    shared_items = find_shared_items_for_part_2(parsed_input)
    priority_sum = compute_priority_sum(shared_items)
    return priority_sum


def compute_priority_sum(shared_items):
    lowercase_letters = "".join(chr(x) for x in range(ord("a"), ord("z") + 1))
    uppercase_letters = "".join(chr(x) for x in range(ord("A"), ord("Z") + 1))
    letters = lowercase_letters + uppercase_letters
    priorities = dict(zip(letters, range(1, len(letters) + 1)))
    priority_sum = sum(priorities[si] for si in shared_items)
    return priority_sum


def find_shared_items_for_part_1(parsed_input: ProblemDataType) -> tuple[int, ...]:
    return tuple(find_shared_item(set(p[0]), set(p[1])) for p in parsed_input)


def find_shared_items_for_part_2(parsed_input: ProblemDataType) -> tuple[int, ...]:
    max_iter = len(parsed_input) // 3

    return tuple(
        find_shared_items_for_group(parsed_input, group_index)
        for group_index in range(max_iter)
    )


def find_shared_items_for_group(parsed_input, group_index):
    group = parsed_input[3 * group_index : 3 * (group_index + 1)]
    group_set = tuple(set(t[0] + t[1]) for t in group)
    shared_items = find_shared_item(*group_set)
    return shared_items


def find_shared_item(*sets: set[str]) -> int:
    intersection = set.intersection(*sets)
    assert len(intersection) == 1
    return intersection.pop()


def parse_input_text_file() -> ProblemDataType:
    text = load_input_text_file(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> ProblemDataType:
    lines = text.strip().split("\n")
    tuples = tuple((p[: len(p) // 2], p[len(p) // 2 : len(p)]) for p in lines)
    return tuples


if __name__ == "__main__":
    main()
