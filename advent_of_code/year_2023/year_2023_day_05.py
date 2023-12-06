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


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    almanac = parse_input_text_file()
    return almanac.find_lowest_number_for_category("location")


def compute_part_2():
    almanac = parse_input_text_file()

    mapping = almanac.maps[0]
    for seed_range in almanac.seed_ranges:
        for mapping_range in mapping.ranges:
            ...
        ...
    # return almanac.find_lowest_number_for_seed_ranges_bruteforce()


def parse_input_text_file() -> Almanac:
    text = load_input_text_file(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> Almanac:
    return parse_almanac(text)


if __name__ == "__main__":
    main()
