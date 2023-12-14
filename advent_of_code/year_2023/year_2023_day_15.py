import numpy as np

from advent_of_code.common import load_input_text_file

ProblemDataType = list[str]

# NORTH = 0
# WEST = 1
# SOUTH = 2
# EAST = 3


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    data = parse_input_text_file()
    list_of_str = get_list_of_str(data, 3)  # initial rotation of 270 degrees
    result = compute_total_load(list_of_str)
    return result


def compute_part_2():
    data = parse_input_text_file()
    return None


def compute_total_load(parsed_input: ProblemDataType):
    minimal_repr = get_minimal_representation(parsed_input)
    sum_of_loads = sum(sum(sum_rock_values(*y) for y in x) for x in minimal_repr)
    return sum_of_loads


def update_state(parsed_input: ProblemDataType) -> np.ndarray:
    minimal_repr = get_minimal_representation(parsed_input)
    rendered_lines = minimal_to_list_of_str(minimal_repr)
    next_arr = np.array([np.fromstring(line, dtype="<S1") for line in rendered_lines])
    return next_arr


def minimal_to_list_of_str(minimal_repr: list[list[tuple[int, int]]]) -> list[str]:
    rendered_lines = []
    for line in minimal_repr:
        parts = []
        pgoal, plength = line[0]
        parts.append("." * (pgoal - plength) + "O" * plength)
        for i in range(1, len(line)):
            cgoal, clength = line[i]
            totlen = cgoal - pgoal - 1
            parts.append("." * (totlen - clength) + "O" * clength)
            pgoal, plength = cgoal, clength
        rendered_line = "#".join(parts)
        rendered_lines.append(rendered_line)
    return rendered_lines


def get_minimal_representation(
    parsed_input: ProblemDataType,
) -> list[list[tuple[int, int]]]:
    split = [line.split("#") for line in parsed_input]
    cube_rock_indices = tuple(
        tuple((*(idx for idx, c in enumerate(li) if c == "#"), len(li)))
        for li in parsed_input
    )
    round_rock_counts = tuple(
        tuple(sum(el == "O" for el in li) for li in line) for line in split
    )
    minimal_repr = [
        list((goal, length) for goal, length in zip(idx, rock_count))
        for idx, rock_count in zip(cube_rock_indices, round_rock_counts)
    ]

    return minimal_repr


def sum_rock_values(goal: int, length: int) -> int:
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
    return input_array


def run_one_full_cycle(parsed_input: np.ndarray, rot: int) -> np.ndarray:
    # North (initial starting rot = 3)
    rot -= 1
    list_of_str = get_list_of_str(parsed_input, rot)
    next_arr = update_state(list_of_str)
    next_arr = np.rot90(next_arr, 4 - rot)

    # West
    rot -= 1
    list_of_str = get_list_of_str(next_arr, rot)
    next_arr = update_state(list_of_str)
    next_arr = np.rot90(next_arr, 4 - rot)

    # South
    rot -= 1
    list_of_str = get_list_of_str(next_arr, rot)
    next_arr = update_state(list_of_str)
    next_arr = np.rot90(next_arr, 4 - rot)

    # East
    rot -= 1
    list_of_str = get_list_of_str(next_arr, rot)
    next_arr = update_state(list_of_str)
    next_arr = np.rot90(next_arr, 4 - rot)

    return next_arr


# def get_list_of_str(
#     input_array: np.ndarray, direction: Literal[0, 1, 2, 3]
# ) -> list[str]:
#     direction = NORTH
#     tolist = np.rot90(input_array, 1 + direction).tolist()
#     # # .T a priori only for north and south
#     # if direction == NORTH or direction == SOUTH:
#     #     tolist = input_array.T.tolist()
#     # else:
#     #     tolist = input_array.tolist()

#     # reversed a priori only for north and west
#     if direction == NORTH or direction == WEST:
#         data = ["".join(i.decode() for i in reversed(li)) for li in tolist]
#     else:
#         data = ["".join(i.decode() for i in li) for li in tolist]


#     return data
def get_list_of_str(input_array: np.ndarray, times: int) -> list[str]:
    if times > 0:
        arr = np.rot90(input_array, times)
    else:
        arr = input_array
    tolist = arr.tolist()
    data = ["".join(i.decode() for i in li) for li in tolist]
    return data


if __name__ == "__main__":
    main()
