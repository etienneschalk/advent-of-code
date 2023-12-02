from pathlib import Path

from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class Handful:  # poignée
    red: int = 0
    green: int = 0
    blue: int = 0


@dataclass(frozen=True, kw_only=True)
class Game:
    identifier: int
    handfuls: list[Handful]


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    games = load_input_text_file()


def compute_part_2():
    ...


def load_input_text_file() -> list[Game]:
    input_path = "resources/advent_of_code/year_2023/input_year_2023_day_2.txt"
    input_path = Path(input_path)
    assert input_path.is_file()
    text = input_path.read_text()
    games = parse_text_input(text)
    assert len(games) == 100
    return games


def parse_text_input(text: str) -> list[Game]:
    game_str_list = text.strip().split("\n")
    return [parse_game_str(game_str) for game_str in game_str_list]


def parse_game_str(game_str: str) -> Game:
    parts = game_str.split(": ")
    identifier = int(parts[0].split(" ")[-1])
    handful_list = [
        parse_handful_str(handful_str) for handful_str in parts[1].split("; ")
    ]
    return Game(identifier=identifier, handfuls=handful_list)


def parse_handful_str(handful_str: str) -> Handful:
    parts = handful_str.split(", ")
    mapping = dict(part.split(" ")[::-1] for part in parts)
    mapping = {k: int(v) for k, v in mapping.items()}
    return Handful(**mapping)
