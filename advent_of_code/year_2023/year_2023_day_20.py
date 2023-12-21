from dataclasses import dataclass
import queue
from advent_of_code.common import load_input_text_file

ProblemDataType = ...

test_data = """

broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a

"""

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

    def send(self, modules: dict[str, "Module"]):
        ...

    def send_to_all(self, pulse: Pulse, modules: dict[str, "Module"]):
        for dest_name in self.destination_names:
            modules[dest_name].receive(self.name, pulse)

    def receive(self, input_name: str, pulse: Pulse):
        pass


@dataclass(kw_only=True)
class BroadcasterModule(Module):
    ...


@dataclass(kw_only=True)
class FlipFlopModule(Module):
    state: FlipFlopState
    next_state: FlipFlopState
    # pulses_to_send: queue.Queue
    pulses_to_send: list[Pulse]

    @staticmethod
    def init(name: str, destination_names: tuple[str]) -> "FlipFlopModule":
        return FlipFlopModule(
            name=name,
            destination_names=destination_names,
            state=Off,
            pulses_to_send=[],
            next_state=Off
            # pulses_to_send=queue.Queue(),
        )

    def receive(self, input_name: str, pulse: Pulse):
        if pulse is LowPulse:
            self.next_state = not self.next_state
            self.pulses_to_send.append(self.next_state)
            # self.pulses_to_send.put(self.state)

    def send(self, modules: dict[str, "Module"]):
        # if queue.empty():
        #     return
        self.state = self.next_state
        if not self.pulses_to_send:
            return
        pulse = self.pulses_to_send.pop(0)
        # pulse = self.pulses_to_send.get()
        super().send_to_all(pulse, modules)


@dataclass(kw_only=True)
class ConjunctionModule(Module):
    prefix = "&"
    inputs: dict[str, Pulse]
    next_inputs: dict[str, Pulse]
    pulses_to_send: list[Pulse]
    next_pulses_to_send: list[Pulse]

    @staticmethod
    def init(name: str, destination_names: tuple[str]) -> "ConjunctionModule":
        return ConjunctionModule(
            name=name,
            destination_names=destination_names,
            inputs={},
            next_inputs={},
            # inputs={name: LowPulse for name in destination_names},
            pulses_to_send=[],
            next_pulses_to_send=[],
        )

    def receive(self, input_name: str, pulse: Pulse):
        self.next_inputs[input_name] = pulse
        pulse = not all(input is HighPulse for input in self.next_inputs.values())
        self.pulses_to_send.append(pulse)

    def send(self, modules: dict[str, "Module"]):
        self.inputs = self.next_inputs
        self.next_inputs = {**self.inputs}

        # if queue.empty():
        #     return
        if not self.pulses_to_send:
            return
        pulse = self.pulses_to_send.pop(0)
        super().send_to_all(pulse, modules)


def main():
    result_part_1 = compute_part_1()
    result_part_2 = compute_part_2()
    print({1: result_part_1, 2: result_part_2})


def compute_part_1():
    # text = load_input_text_file(__file__)
    text = test_data
    modules = parse_text_input(text)
    modules["broadcaster"].send_to_all(LowPulse, modules)
    ...
    for name, module in modules.items():
        module.send(modules)
    ...
    for name, module in modules.items():
        module.send(modules)
    ...
    for name, module in modules.items():
        module.send(modules)
    ...
    for name, module in modules.items():
        module.send(modules)
    return None


def compute_part_2():
    text = load_input_text_file(__file__)
    parsed = parse_text_input(text)
    ...
    return None


def parse_text_input(text: str) -> ProblemDataType:
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

        module = module_class.init(
            name=name, destination_names=tuple(destinations.split(", "))
        )

        modules[name] = module
    ...
    return modules


if __name__ == "__main__":
    main()
