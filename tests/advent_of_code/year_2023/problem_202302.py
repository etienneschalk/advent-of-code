from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.year_2023.problem_202302 import (
    Game,
    Handful,
    compute_minimal_required_handful,
    compute_possible_games,
    parse_text_input,
)


def test_problem_20232_part_1(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    games = parse_text_input(test_input)

    assert len(games) == 5
    assert games == [
        Game(
            identifier=1,
            handfuls=[
                Handful(red=4, green=0, blue=3),
                Handful(red=1, green=2, blue=6),
                Handful(red=0, green=2, blue=0),
            ],
        ),
        Game(
            identifier=2,
            handfuls=[
                Handful(red=0, green=2, blue=1),
                Handful(red=1, green=3, blue=4),
                Handful(red=0, green=1, blue=1),
            ],
        ),
        Game(
            identifier=3,
            handfuls=[
                Handful(red=20, green=8, blue=6),
                Handful(red=4, green=13, blue=5),
                Handful(red=1, green=5, blue=0),
            ],
        ),
        Game(
            identifier=4,
            handfuls=[
                Handful(red=3, green=1, blue=6),
                Handful(red=6, green=3, blue=0),
                Handful(red=14, green=3, blue=15),
            ],
        ),
        Game(
            identifier=5,
            handfuls=[Handful(red=6, green=3, blue=1), Handful(red=1, green=2, blue=2)],
        ),
    ]

    # 12 red cubes, 13 green cubes, and 14 blue cubes
    # a bag is a handful too
    reference_bag = Handful(red=12, green=13, blue=14)
    possible_games = compute_possible_games(reference_bag, games)
    possible_games_identifiers = [g.identifier for g in possible_games]
    assert possible_games_identifiers == [1, 2, 5]
    assert sum(possible_games_identifiers) == 8


def test_problem_20232_part_2(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    games = parse_text_input(test_input)

    # 12 red cubes, 13 green cubes, and 14 blue cubes
    # a bag is a handful too
    expected_minimal_handfuls = [
        Handful(red=4, green=2, blue=6),
        Handful(red=1, green=3, blue=4),
        Handful(red=20, green=13, blue=6),
        Handful(red=14, green=3, blue=15),
        Handful(red=6, green=3, blue=2),
    ]

    for game, expected_minimal_handful in zip(games, expected_minimal_handfuls):
        assert compute_minimal_required_handful(game) == expected_minimal_handful

    expected_powers = [48, 12, 1560, 630, 36]
    assert [h.power for h in expected_minimal_handfuls] == expected_powers
