from advent_of_code.year_2023.year_2023_day_17 import State, dijkstra, parse_text_input

EXAMPLE_INPUT = """

2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533

"""

EXAMPLE_INPUT_PART_2 = """

111111111111
999999999991
999999999991
999999999991
999999999991

"""


def test_year_2023_day_17_misc():
    # Heat excluded from hash, but included in comparison
    assert hash(State(10, (0, 0), 0, 0)) == hash(State(99999, (0, 0), 0, 0))
    assert (State(10, (0, 0), 0, 0)) < (State(99999, (0, 0), 0, 0))
    assert (State(10, (0, 0), 0, 0)) in {(State(10, (0, 0), 0, 0))}
    # Unexpected behaviour: the heat should be ignored from hash... it seems not
    assert (State(10, (0, 0), 0, 0)) not in {(State(99999, (0, 0), 0, 0))}
    # Expected
    assert (State(10, (0, 0), 0, 0)) not in {(State(10, (1, 2), 3, 4))}

    # Workaround: dict of hash
    initial_state = State(10, (0, 0), 0, 0)
    dicthashmap = {hash(initial_state): initial_state}
    different_heat_state = State(99999, (0, 0), 0, 0)
    assert hash(different_heat_state) == hash(initial_state)
    assert hash(different_heat_state) in dicthashmap
    assert dicthashmap[hash(different_heat_state)] == initial_state
    dicthashmap[hash(different_heat_state)] = different_heat_state
    assert dicthashmap[hash(different_heat_state)] == different_heat_state


def test_year_2023_day_17_part_1():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)

    start = (0, 0)
    end = tuple((parsed_input.shape[0] - 1, parsed_input.shape[1] - 1))
    least_heat_loss = dijkstra(parsed_input, start, end, 1, 3)
    assert least_heat_loss == 102


def test_year_2023_day_17_part_2_a():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)

    start = (0, 0)
    end = tuple((parsed_input.shape[0] - 1, parsed_input.shape[1] - 1))
    least_heat_loss = dijkstra(parsed_input, start, end, 4, 10)
    assert least_heat_loss == 94


def test_year_2023_day_17_part_2_b():
    test_input = EXAMPLE_INPUT_PART_2
    parsed_input = parse_text_input(test_input)

    start = (0, 0)
    end = tuple((parsed_input.shape[0] - 1, parsed_input.shape[1] - 1))
    least_heat_loss = dijkstra(parsed_input, start, end, 4, 10)
    assert least_heat_loss == 71
