from abc import abstractmethod
from dataclasses import dataclass
from typing import Literal, get_args

import numpy as np

from advent_of_code.common.common import load_input_text_file_from_filename
from advent_of_code.common.protocols import AdventOfCodeProblem

LowPulseType = Literal[False]
HighPulseType = Literal[True]
type Pulse = Literal[LowPulseType, HighPulseType]

OffType = LowPulseType
OnType = HighPulseType
type FlipFlopState = Literal[OffType, OnType]

LowPulse = get_args(LowPulseType)[0]
HighPulse = get_args(HighPulseType)[0]
Off = get_args(OffType)[0]
On = get_args(OnType)[0]

type PuzzleInput = str


@dataclass(kw_only=True)
class AdventOfCodeProblem202320(AdventOfCodeProblem[PuzzleInput]):
    year: int = 2023
    day: int = 20

    @staticmethod
    def parse_text_input(text: str) -> PuzzleInput:
        return text

    def solve_part_1(self, puzzle_input: PuzzleInput):
        start_module_dict = parse_text_to_module_dict(puzzle_input)
        module_dict = parse_text_to_module_dict(puzzle_input)

        histories = compute_successive_histories_until_circle_back(
            start_module_dict, module_dict, 1000
        )

        result = compute_result_for_part_1(histories, 1000)

        return result

    def solve_part_2(self, puzzle_input: PuzzleInput):
        module_dict = parse_text_to_module_dict(puzzle_input)

        max_iter = 5000

        # hb is the parent of rx
        events_of_interest = detect_periods_part_2(module_dict, max_iter, "hb")

        periods = [t[0] for t in events_of_interest]
        product = int(np.prod(periods))

        # Use LCM for safety. We could have had some periods that are multiples between each others.
        lcm = int(np.lcm.reduce(periods))
        assert product == lcm

        return int(product)


@dataclass(kw_only=True)
class Module:
    prefix = ""
    name: str
    destination_names: tuple[str, ...]

    @staticmethod
    def init(name: str, destination_names: tuple[str, ...]) -> "Module":
        return Module(
            name=name,
            destination_names=destination_names,
        )

    @abstractmethod
    def receive(self, source: str, pulse: Pulse) -> list["Message"]:
        pass


ModuleDict = dict[str, Module]


@dataclass(frozen=True, kw_only=True)
class Message:
    # source: Module
    # destination: Module
    # pulse: Pulse
    source: str
    destination: str
    pulse: Pulse

    def __repr__(self) -> str:
        pulse_str = "high" if self.pulse else "low"
        return f"{self.source} -{pulse_str}-> {self.destination}"


@dataclass(kw_only=True)
class BroadcasterModule(Module):
    @staticmethod
    def init(name: str, destination_names: tuple[str, ...]) -> "BroadcasterModule":
        return BroadcasterModule(
            name=name,
            destination_names=destination_names,
        )

    def receive(self, source: str, pulse: Pulse) -> list[Message]:
        messages = [
            Message(source=self.name, destination=dest, pulse=pulse)
            for dest in self.destination_names
        ]
        return messages


@dataclass(kw_only=True)
class FlipFlopModule(Module):
    state: FlipFlopState
    pulses_to_send: list[Pulse]

    @staticmethod
    def init(name: str, destination_names: tuple[str, ...]) -> "FlipFlopModule":
        return FlipFlopModule(
            name=name,
            destination_names=destination_names,
            state=Off,
            pulses_to_send=[],
        )

    def receive(self, source: str, pulse: Pulse) -> list[Message]:
        if pulse == LowPulse:
            self.state = not self.state
            pulse = self.state
            return [
                Message(source=self.name, destination=dest, pulse=pulse)
                for dest in self.destination_names
            ]
        return []


@dataclass(kw_only=True)
class ConjunctionModule(Module):
    prefix = "&"
    inputs: dict[str, Pulse]
    pulses_to_send: list[Pulse]

    @staticmethod
    def init(name: str, destination_names: tuple[str, ...]) -> "ConjunctionModule":
        return ConjunctionModule(
            name=name,
            destination_names=destination_names,
            inputs={},
            pulses_to_send=[],
        )

    def receive(self, source: str, pulse: Pulse) -> list[Message]:
        self.inputs[source] = pulse
        pulse = not all(input == HighPulse for input in self.inputs.values())
        return [
            Message(source=self.name, destination=dest, pulse=pulse)
            for dest in self.destination_names
        ]


def load_input_text_file_y2023_d20() -> str:
    return load_input_text_file_from_filename(__file__)


def compute_simulation_history(modules: ModuleDict):
    messages = [Message(source="button", destination="broadcaster", pulse=LowPulse)]
    history = [*messages]

    while messages:
        message = messages.pop(0)
        module = modules.get(message.destination, None)
        if module is None:
            continue
        response = module.receive(message.source, message.pulse)
        messages.extend(response)
        history.extend(response)

    return history


def compute_result_for_part_1(
    histories: list[list[Message]], button_push_count: int
) -> int:
    high_pulse_count_total = 0
    low_pulse_count_total = 0
    cycle_length = len(histories)
    for h in histories:
        high_pulse_count = sum(m.pulse for m in h)
        low_pulse_count = len(h) - high_pulse_count
        high_pulse_count_total += high_pulse_count
        low_pulse_count_total += low_pulse_count
    result = (
        (button_push_count // cycle_length) ** 2
        * high_pulse_count_total
        * low_pulse_count_total
    )
    return result


def compute_successive_histories_until_circle_back(
    start_module_dict: ModuleDict,
    module_dict: ModuleDict,
    max_iter: int = 1000,
    *,
    keep_history: bool = True,
):
    i = 0
    histories: list[list[Message]] = []
    while i < max_iter and (module_dict != start_module_dict or i == 0):
        i += 1
        history = compute_simulation_history(module_dict)
        if keep_history:
            histories.append(history)

    return histories


def detect_periods_part_2(
    module_dict: ModuleDict,
    max_iter: int = 5000,
    target_module: str = "hb",
) -> list[tuple[int, Message]]:
    i = 0
    conjunction_module = module_dict[target_module]
    assert isinstance(conjunction_module, ConjunctionModule)
    modules_of_interest = {n: [] for n in conjunction_module.inputs}
    expected_messages = {
        n: Message(source=n, destination=target_module, pulse=HighPulse)
        for n in modules_of_interest
    }.values()
    events_of_interest = []
    while i < max_iter:
        i += 1
        history = compute_simulation_history(module_dict)
        for msg in expected_messages:
            if msg in history:
                events_of_interest.append((i, msg))
        if len(events_of_interest) == len(modules_of_interest):
            return events_of_interest
    return events_of_interest


def parse_text_to_module_dict(text: str) -> ModuleDict:
    lines = text.strip().split("\n")

    modules: dict[str, Module] = {}
    for line in lines:
        name, destinations = line.split(" -> ")

        if name[0] == "&":
            module_class = ConjunctionModule
            name = name[1:]
        elif name[0] == "%":
            module_class = FlipFlopModule
            name = name[1:]
        elif name == "broadcaster":
            module_class = BroadcasterModule
        else:
            module_class = Module

        candidate = module_class.init(
            name=name, destination_names=tuple(destinations.split(", "))
        )

        modules[name] = candidate

    # Initialize Conjunction sources
    conjunction_modules = []
    for m in modules.values():
        if type(m) is ConjunctionModule:
            conjunction_modules.append(m)
    for conj in conjunction_modules:
        for module in modules.values():
            if conj.name in module.destination_names:
                conj.inputs[module.name] = False
    ...
    return modules


if __name__ == "__main__":
    print(AdventOfCodeProblem202320().solve())
