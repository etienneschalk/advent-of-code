import pytest

from advent_of_code.year_2023.year_2023_day_05 import (
    AlmanacMap,
    AlmanacRange,
    parse_almanac,
)

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


def test_year_2023_day_5_part_1_parse_almanac():
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


@pytest.mark.skip(reason="not implemented yet")
def test_year_2023_day_5_part_2_parse_almanac():
    almanac = parse_almanac(EXAMPLE_INPUT)
    assert almanac.seeds == [79, 14, 55, 13]
    assert almanac.seed_ranges == [range(79, 79 + 14), range(55, 55 + 13)]

    assert almanac.find_lowest_number_for_seed_ranges_bruteforce() == 46

    # all_ = list(almanac.unroll_almanac_dict(i)["location"] for i in range(100))

    mapped_ranges = []
    mapping = almanac.maps[0]
    for seed_range in almanac.seed_ranges:
        for mapping_range in mapping.ranges:
            maxmin = max(min(seed_range), min(mapping_range.source_range))
            # maxmin_inside = maxmin in seed_range
            minmax = min(max(seed_range), max(mapping_range.source_range)) + 1
            # minmax_inside = minmax in seed_range
            print(f"{maxmin=}, {minmax=}")
            # print(f"{maxmin_inside}")
            # print(f"{minmax}")
            # print(f"{minmax_inside}")
            possible_range = maxmin < minmax
            print(f"{possible_range=}")
            if possible_range:
                delta = (
                    mapping_range.destination_range_start
                    - mapping_range.source_range_start
                )
                mapped_range = range(maxmin + delta, minmax + delta)
                mapped_ranges.append(mapped_range)
            ...
    ...
    # 55: 86
    # 56: 87
    # 57: 88
    # 58: 89
    # 59: 94
    # 60: 95
    # 61: 96
    # 62: 56
    # 63: 57
    # 64: 58
    # 65: 59
    # 66: 97
    # 67: 98

    # 79: 82
    # 80: 83
    # 81: 84
    # 82: 46
    # 83: 47
    # 84: 48
    # 85: 49
    # 86: 50
    # 87: 51
    # 88: 52
    # 89: 53
    # 90: 54
    # 91: 55
    # 92: 60


# def map_ranges(input_ranges: list[range], mapping: AlmanacMap) -> list[range]:
#     funnel_source_ranges = [r.source_range for r in mapping.ranges]
#     sort_mapping_by_source_range_start_in_place(mapping.ranges)
#     # funnel_destination_ranges = [r.destination_range for r in mapping.ranges]
#     initial_cursor = min(min(input_ranges[0]), min(funnel_source_ranges[0]))
#     cursor = initial_cursor
#     in_input_range = False
#     in_funnel_source_range = False
#     cursor = 0
#     current_input_range = input_ranges.pop(0)
#     current_funnel_source_range = funnel_source_ranges.pop(0)
#     while input_ranges and funnel_source_ranges:
#         if in_input_range:
#             mark_i = max(current_input_range)
#         else:
#             mark_i = min(current_input_range)
#         if in_funnel_source_range:
#             mark_f = max(current_funnel_source_range)
#         else:
#             mark_f = min(current_funnel_source_range)
#         if mark_i <= mark_f:
#             in_input_range = not in_input_range
#         if mark_i >= mark_f:
#             in_funnel_source_range = True
#         cursor = min(mark_i, mark_f)
#         ...
#         # if not in_input_range and not in_funnel_source_range:
#         #     min_i = min(current_input_range)
#         #     min_f = min(current_funnel_source_range)
#         #     cursor = min(min_i, min_f)
#         #     if min_i <= min_f:
#         #         in_input_range = True
#         #     if min_i >= min_f:
#         #         in_funnel_source_range = True
#         #     ...
#         # elif not in_input_range and in_funnel_source_range:

#     ...


def map_ranges(input_ranges: list[range], mapping: AlmanacMap) -> list[range]:
    sort_mapping_by_source_range_start_in_place(mapping.ranges)
    intersections_of_input_ranges = []
    for input_range in input_ranges:
        intersections = [
            intersect_ranges(input_range, mr.source_range) for mr in mapping.ranges
        ]
        intersections_of_input_ranges.append(intersections)
        ...
    mapped_input_ranges = []
    for index, mapping_range in enumerate(mapping.ranges):
        input_ranges_split = [i[index] for i in intersections_of_input_ranges]
        delta = mapping_range.destination_range_start - mapping_range.source_range_start
        mapped = [range(r.start + delta, r.stop + delta) for r in input_ranges_split]
        mapped_input_ranges.append(mapped)
        ...
    flattened_filtered_ranges = [
        y for x in mapped_input_ranges for y in x if y.start < y.stop
    ]
    sort_ranges_in_place(flattened_filtered_ranges)
    return flattened_filtered_ranges


def intersect_ranges(range_a: range, range_b: range) -> range:
    a = range_a
    b = range_b
    return range(max(a.start, b.start), min(a.stop, b.stop))


def sort_mapping_by_source_range_start_in_place(
    almanac_ranges: list[AlmanacRange],
) -> AlmanacRange:
    almanac_ranges.sort(key=lambda ar: ar.source_range_start)


def sort_ranges_in_place(ranges: list[range]):
    ranges.sort(key=lambda r: min(r))


def test_year_2023_day_5_part_2_second_try():
    almanac = parse_almanac(EXAMPLE_INPUT)
    assert almanac.seeds == [79, 14, 55, 13]
    assert almanac.seed_ranges == [range(79, 79 + 14), range(55, 55 + 13)]
    assert almanac.seed_ranges == [range(79, 93), range(55, 68)]
    sort_ranges_in_place(almanac.seed_ranges)
    assert almanac.seed_ranges == [range(55, 68), range(79, 93)]

    assert almanac.maps[0].ranges == [
        AlmanacRange(destination_range_start=50, source_range_start=98, range_length=2),
        AlmanacRange(
            destination_range_start=52, source_range_start=50, range_length=48
        ),
    ]

    sort_mapping_by_source_range_start_in_place(almanac.maps[0].ranges)
    assert almanac.maps[0].ranges == [
        AlmanacRange(
            destination_range_start=52, source_range_start=50, range_length=48
        ),
        AlmanacRange(destination_range_start=50, source_range_start=98, range_length=2),
    ]

    first_map = map_ranges(almanac.seed_ranges, almanac.maps[0])
    assert first_map == [range(57, 70), range(81, 95)]
