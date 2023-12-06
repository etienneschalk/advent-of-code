from dataclasses import dataclass
from functools import cached_property

from advent_of_code.common import load_input_text_file


@dataclass(frozen=True)
class AlmanacRange:
    destination_range_start: int
    source_range_start: int
    range_length: int

    @property
    def destination_range(self):
        start = self.destination_range_start
        return range(start, start + self.range_length)

    @property
    def source_range(self):
        start = self.source_range_start
        return range(start, start + self.range_length)

    def is_source_in_source_range(self, source: int) -> bool:
        return source in self.source_range

    def source_to_target(self, source: int) -> int:
        if self.is_source_in_source_range(source):
            delta = source - self.source_range_start
            return delta + self.destination_range_start
        return source


@dataclass(frozen=True, kw_only=True)
class AlmanacMap:
    source_category: str
    destination_category: str
    ranges: list[AlmanacRange]

    def source_to_target(self, source: int) -> int:
        for almanac_range in self.ranges:
            if almanac_range.is_source_in_source_range(source):
                return almanac_range.source_to_target(source)
        return source


@dataclass(frozen=True, kw_only=True)
class Almanac:
    seeds: list[int]
    maps: list[AlmanacMap]

    def unroll_almanac_dict(self, source: int) -> dict[str, int]:
        path: dict[str, int] = {}
        path[self.maps[0].source_category] = source
        destination = source
        for almanac_map in self.maps:
            destination = almanac_map.source_to_target(destination)
            path[almanac_map.destination_category] = destination
        return path

    def unroll_almanac_part_2(self, source: int) -> dict[str, int]:
        destination = source
        for almanac_map in self.maps:
            destination = almanac_map.source_to_target(destination)
        return destination

    def find_lowest_number_for_category(self, category: str) -> int:
        return min(self.unroll_almanac_dict(seed)[category] for seed in self.seeds)

    @cached_property
    def seed_ranges(self) -> list[range]:
        seeds = self.seeds
        seed_ranges = list(
            range(start, start + offset)
            for start, offset in (zip(seeds[::2], seeds[1::2]))
        )
        return seed_ranges

    def find_lowest_number_for_seed_ranges_bruteforce(self):
        print(f"Seed Ranges: {self.seed_ranges}")
        print(f"Range Lengths: {[len(r) for r in self.seed_ranges]}")
        print(f"Seed Count: {sum([len(r)for r in self.seed_ranges]):e}")
        mins = []
        for seed_range in self.seed_ranges:
            print(f"Seed Range: {seed_range} | Length: {len(seed_range): e}")
            the_min = min(self.unroll_almanac_part_2(seed) for seed in seed_range)
            mins.append(the_min)
        return min(*mins)
        # seed_gen = (b for a in (list(r) for r in self.seed_ranges) for b in a)
        # return min(self.unroll_almanac_dict_part_2(seed) for seed in seed_gen)


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    almanac = parse_input_text_file()
    return almanac.find_lowest_number_for_category("location")


def compute_part_2():
    almanac = parse_input_text_file()
    return compute_lowest_location_number(almanac)


def compute_lowest_location_number(almanac: Almanac) -> int:
    # Fill holes in mappings and create identity mappings for them
    fill_almanac_in_place(almanac)
    # Sort input ranges
    sort_ranges_in_place(almanac.seed_ranges)  # sort inputs

    input_ranges = almanac.seed_ranges

    tree = recur_map_ranges_tree(almanac, input_ranges)

    min_location_number = find_min_range_in_tree(tree)

    return min_location_number


def find_min_range_in_tree(tree: range | list):
    if isinstance(tree, range):
        return tree.start
    elif isinstance(tree, list):
        return min(find_min_range_in_tree(el) for el in tree)


def recur_map_ranges_tree(
    almanac: Almanac, input_ranges: list[range], almanac_map_index: int = 0
):
    if almanac_map_index >= len(almanac.maps):
        return input_ranges
    mapping = almanac.maps[almanac_map_index]
    range_tree = map_ranges_tree(input_ranges, mapping)
    return [
        recur_map_ranges_tree(almanac, range_tree_el, almanac_map_index + 1)
        for range_tree_el in range_tree
    ]


def map_ranges_tree(
    input_ranges: list[range], mapping: AlmanacMap
) -> list[list[range]]:
    sort_mapping_by_source_range_start_in_place(mapping.ranges)
    # (input, input ^ source )
    intersections_of_input_ranges = []
    mapped_intersections_of_input_ranges = []
    for input_range in input_ranges:
        intersections = [
            intersect_ranges(input_range, mr.source_range) for mr in mapping.ranges
        ]
        intersections_of_input_ranges.append(intersections)
        mapped_list = []
        for intersection, mapping_range in zip(intersections, mapping.ranges):
            delta = (
                mapping_range.destination_range_start - mapping_range.source_range_start
            )
            mapped = range(intersection.start + delta, intersection.stop + delta)
            if mapped.start < mapped.stop:
                mapped_list.append(mapped)
        mapped_intersections_of_input_ranges.append(mapped_list)
    return mapped_intersections_of_input_ranges


def intersect_ranges(range_a: range, range_b: range) -> range:
    a = range_a
    b = range_b
    return range(max(a.start, b.start), min(a.stop, b.stop))


def sort_mapping_by_source_range_start_in_place(
    almanac_ranges: list[AlmanacRange],
) -> AlmanacRange:
    almanac_ranges.sort(key=lambda ar: ar.source_range_start)


def sort_ranges_in_place(ranges: list[range]):
    ranges.sort(key=lambda r: r.start)


# DONE detect max possible value in the Almanac
# DONE clean to fill hole in mapping with an id mapping
def find_max_destination_stop_in_almanac(almanac: Almanac) -> int:
    return max(find_max_destination_stop_in_almanac_map(am) for am in almanac.maps)


def find_max_destination_stop_in_almanac_map(am: AlmanacMap) -> int:
    return max(find_max_destination_stop_in_almanac_range(r) for r in am.ranges)


def find_max_destination_stop_in_almanac_range(ar: AlmanacRange) -> int:
    return ar.destination_range_start + ar.range_length


def fill_almanac_in_place(almanac: Almanac) -> Almanac:
    max_almanac = find_max_destination_stop_in_almanac(almanac)
    for mapping in almanac.maps:
        fill_almanac_map_in_place(mapping, max_almanac)


def fill_almanac_map_in_place(mapping: AlmanacMap, max_stop: int) -> AlmanacMap:
    # from ....xx..xxx...
    # to   iiii..ii...iii
    sort_mapping_by_source_range_start_in_place(mapping.ranges)
    boundaries = [
        0,
        *(
            (
                y
                for x in (
                    (mr.source_range.start, mr.source_range.stop)
                    for mr in mapping.ranges
                )
                for y in x
            )
        ),
        max_stop,
    ]
    identity_ranges = [
        range(start, stop)
        for start, stop in (zip(boundaries[::2], boundaries[1::2]))
        if start < stop
    ]
    identity_almanac_ranges = [
        AlmanacRange(
            destination_range_start=r.start,
            source_range_start=r.start,
            range_length=r.stop,
        )
        for r in identity_ranges
    ]
    mapping.ranges.extend(identity_almanac_ranges)
    sort_mapping_by_source_range_start_in_place(mapping.ranges)


def parse_input_text_file() -> Almanac:
    text = load_input_text_file(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> Almanac:
    return parse_almanac(text)


def parse_almanac_range(line: str) -> AlmanacRange:
    return AlmanacRange(*(int(i) for i in line.split(" ")))


def parse_almanac_map(lines: list[str]) -> AlmanacMap:
    categories = lines[0].split(" ")[0].split("-")
    source_category, destination_category = categories[0], categories[-1]
    ranges = [parse_almanac_range(line) for line in lines[1:]]
    return AlmanacMap(
        source_category=source_category,
        destination_category=destination_category,
        ranges=ranges,
    )


def parse_almanac(text: str) -> Almanac:
    sections = text.strip().split("\n\n")
    seeds = [int(i) for i in sections[0].split(" ", 1)[-1].split(" ")]
    maps = [parse_almanac_map(section.split("\n")) for section in sections[1:]]
    return Almanac(seeds=seeds, maps=maps)


def map_ranges_prototype(input_ranges: list[range], mapping: AlmanacMap) -> list[range]:
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


if __name__ == "__main__":
    main()
