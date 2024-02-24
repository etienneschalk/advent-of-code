from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.y_2023.problem_202306 import (
    compute_number_of_ways_to_win,
    correct_data,
    parse_text_input,
)


def test_problem_20236_part_intro():
    races = [
        {"time": 7, "distance": 9},
        {"time": 15, "distance": 40},
        {"time": 30, "distance": 200},
    ]

    first_race = races[0]
    t = first_race["time"]
    current_record = first_race["distance"]
    options = {x: x * (t - x) for x in range(t + 1)}
    assert options == {0: 0, 1: 6, 2: 10, 3: 12, 4: 12, 5: 10, 6: 6, 7: 0}
    winnings = [key for key, value in options.items() if value > current_record]
    assert winnings == [2, 3, 4, 5]
    assert len(winnings) == 4

    first_race = races[1]
    t = first_race["time"]
    current_record = first_race["distance"]
    options = {x: x * (t - x) for x in range(t + 1)}
    winnings = [key for key, value in options.items() if value > current_record]
    assert winnings == [4, 5, 6, 7, 8, 9, 10, 11]
    assert len(winnings) == 8

    first_race = races[2]
    t = first_race["time"]
    current_record = first_race["distance"]
    options = {x: x * (t - x) for x in range(t + 1)}
    winnings = [key for key, value in options.items() if value > current_record]
    assert winnings == [11, 12, 13, 14, 15, 16, 17, 18, 19]
    assert len(winnings) == 9


def test_problem_20236_part_1(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    parsed_input = parse_text_input(test_input)  # noqa: F841
    assert parsed_input == {"Time:": [7, 15, 30], "Distance:": [9, 40, 200]}
    number_of_ways = compute_number_of_ways_to_win(parsed_input)
    assert number_of_ways == 288
    ...


def test_problem_20236_part_2(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    parsed_input = parse_text_input(test_input)  # noqa: F841
    data = correct_data(parsed_input)
    assert data == {"Time:": [71530], "Distance:": [940200]}
    number_of_ways = compute_number_of_ways_to_win(data)
    assert number_of_ways == 71503
