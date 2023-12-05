from dataclasses import dataclass

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
        for range_ in self.ranges:
            if range_.is_source_in_source_range(source):
                return range_.source_to_target(source)
        return source


@dataclass(frozen=True, kw_only=True)
class Almanac:
    seeds: list[int]
    maps: list[AlmanacMap]


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
    data = parse_input_text_file()  # noqa: F841
    ...
    return None


def compute_part_2():
    data = parse_input_text_file()  # noqa: F841
    ...
    return None


def parse_input_text_file() -> ...:
    text = load_input_text_file(__file__)
    parsed = parse_text_input(text)
    return parsed


def parse_text_input(text: str) -> ...:
    lines = text.strip().split("\n")
    ...
    return lines


if __name__ == "__main__":
    main()
