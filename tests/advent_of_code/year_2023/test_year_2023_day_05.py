from advent_of_code.year_2023.year_2023_day_00_template import parse_text_input
from advent_of_code.year_2023.year_2023_day_05 import parse_almanac

EXAMPLE_INPUT = """

seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4

"""


def test_parse_almanac():
    almanac = parse_almanac(EXAMPLE_INPUT)
    assert almanac.seeds == [79, 14, 55, 13]

    first_map = almanac.maps[0]

    assert first_map.source_category == "seed"
    assert first_map.destination_category == "soil"

    assert first_map.ranges[0].destination_range_start == 50
    assert first_map.ranges[0].source_range_start == 98
    assert first_map.ranges[0].range_length == 2
    assert first_map.ranges[0].destination_range == range(50, 50 + 2)
    assert first_map.ranges[0].source_range == range(98, 98 + 2)
    assert first_map.ranges[0].source_to_target(98) == 50
    assert first_map.ranges[0].source_to_target(99) == 51

    assert first_map.ranges[1].destination_range_start == 52
    assert first_map.ranges[1].source_range_start == 50
    assert first_map.ranges[1].range_length == 48
    assert first_map.ranges[1].destination_range == range(52, 52 + 48)
    assert first_map.ranges[1].source_range == range(50, 50 + 48)
    assert first_map.ranges[1].source_to_target(53) == 55

    assert first_map.source_to_target(98) == 50
    assert first_map.source_to_target(99) == 51
    assert first_map.source_to_target(53) == 55
    assert first_map.source_to_target(10) == 10  # no mapping

    assert first_map.source_to_target(0) == 0
    assert first_map.source_to_target(1) == 1
    assert first_map.source_to_target(48) == 48
    assert first_map.source_to_target(49) == 49
    assert first_map.source_to_target(50) == 52
    assert first_map.source_to_target(51) == 53
    assert first_map.source_to_target(96) == 98
    assert first_map.source_to_target(97) == 99
    assert first_map.source_to_target(98) == 50
    assert first_map.source_to_target(99) == 51

    assert first_map.source_to_target(79) == 81
    assert first_map.source_to_target(14) == 14
    assert first_map.source_to_target(55) == 57
    assert first_map.source_to_target(13) == 13

    expected_unrolled = {
        79: {
            "seed": 79,
            "soil": 81,
            "fertilizer": 81,
            "water": 81,
            "light": 74,
            "temperature": 78,
            "humidity": 78,
            "location": 82,
        },
        14: {
            "seed": 14,
            "soil": 14,
            "fertilizer": 53,
            "water": 49,
            "light": 42,
            "temperature": 42,
            "humidity": 43,
            "location": 43,
        },
        55: {
            "seed": 55,
            "soil": 57,
            "fertilizer": 57,
            "water": 53,
            "light": 46,
            "temperature": 82,
            "humidity": 82,
            "location": 86,
        },
        13: {
            "seed": 13,
            "soil": 13,
            "fertilizer": 52,
            "water": 41,
            "light": 34,
            "temperature": 34,
            "humidity": 35,
            "location": 35,
        },
    }

    assert all(
        almanac.unroll_almanac_dict(source) == expected
        for source, expected in expected_unrolled.items()
    )

    assert almanac.find_lowest_number_for_category("location") == 35


def test_year_2023_day_5_part_1():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)  # noqa: F841


def test_year_2023_day_5_part_2():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)  # noqa: F841
