from dataclasses import dataclass

from advent_of_code.common import load_input_text_file

LowPulse = False
HighPulse = True
Pulse = LowPulse | HighPulse
Off = False
On = True
FlipFlopState = Off | On


@dataclass(kw_only=True)
class Module:
    prefix = ""
    name: str
    destination_names: tuple[str]

    @staticmethod
    def init(name: str, destination_names: tuple[str]) -> "Module":
        return Module(
            name=name,
            destination_names=destination_names,
        )

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
    def init(name: str, destination_names: tuple[str]) -> "BroadcasterModule":
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
    def init(name: str, destination_names: tuple[str]) -> "FlipFlopModule":
        return FlipFlopModule(
            name=name,
            destination_names=destination_names,
            state=Off,
            pulses_to_send=[],
        )

    def receive(self, source: str, pulse: Pulse) -> list[Message]:
        if pulse is LowPulse:
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
    def init(name: str, destination_names: tuple[str]) -> "ConjunctionModule":
        return ConjunctionModule(
            name=name,
            destination_names=destination_names,
            inputs={},
            pulses_to_send=[],
        )

    def receive(self, source: str, pulse: Pulse) -> list[Message]:
        self.inputs[source] = pulse
        pulse = not all(input is HighPulse for input in self.inputs.values())
        return [
            Message(source=self.name, destination=dest, pulse=pulse)
            for dest in self.destination_names
        ]


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    text = load_input_text_file(__file__)
    # text = test_data
    modules = parse_text_input(text)

    history = compute_simulation_history(modules)

    result = len(history)
    return result


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


def compute_part_2():
    return None


def parse_text_input(text: str) -> ModuleDict:
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
    main()
