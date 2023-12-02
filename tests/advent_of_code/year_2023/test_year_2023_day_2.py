from advent_of_code.year_2023.year_2023_day_2 import (
    compute_possible_games,
    parse_text_input,
    Game,
    Handful,
)


def test_year_2023_day_2_part_1():
    test_input = """
    
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green

"""
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
