from dataclasses import dataclass

from advent_of_code.protocols import AdventOfCodeProblem


@dataclass(frozen=True, kw_only=True)
class Handful:  # poignée
    red: int = 0
    green: int = 0
    blue: int = 0

    @property
    def power(self) -> int:
        return self.red * self.green * self.blue


@dataclass(frozen=True, kw_only=True)
class Game:
    identifier: int
    handfuls: list[Handful]


type PuzzleInput = list[Game]


@dataclass(kw_only=True)
class AdventOfCodeProblem202302(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2023
    day: int = 2

    def solve_part_1(self, puzzle_input: PuzzleInput):
        # 12 red cubes, 13 green cubes, and 14 blue cubes
        # a bag is a handful too
        reference_bag = Handful(red=12, green=13, blue=14)
        possible_games = compute_possible_games(reference_bag, puzzle_input)
        possible_games_identifiers = [g.identifier for g in possible_games]
        answer = sum(possible_games_identifiers)
        return answer

    def solve_part_2(self, puzzle_input: PuzzleInput):
        minimal_handfuls = [
            compute_minimal_required_handful(game) for game in puzzle_input
        ]
        return sum(h.power for h in minimal_handfuls)

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
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


def compute_possible_games(bag: Handful, candidate_games: list[Game]) -> list[Game]:
    possible_games: list[Game] = []
    for game in candidate_games:
        if all(is_handful_possible(bag, handful) for handful in game.handfuls):
            possible_games.append(game)
    return possible_games


def is_handful_possible(bag: Handful, handful: Handful) -> bool:
    return not (
        handful.red > bag.red
        or handful.green > bag.green
        or handful.blue > bag.blue
        or sum((handful.red, handful.blue, handful.green))
        > sum((bag.red, bag.green, bag.blue))
    )


def compute_minimal_required_handful(game: Game) -> Handful:
    return Handful(
        red=max(handful.red for handful in game.handfuls),
        green=max(handful.green for handful in game.handfuls),
        blue=max(handful.blue for handful in game.handfuls),
    )


if __name__ == "__main__":
    print(AdventOfCodeProblem202302().solve_all())
