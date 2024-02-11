import pytest

from advent_of_code.common.common import get_example_inputs_file_contents
from advent_of_code.common.store import ExampleInputsStore


@pytest.fixture(scope="session")
def example_inputs() -> ExampleInputsStore:
    parsed_toml = get_example_inputs_file_contents()
    return ExampleInputsStore(_parsed_toml=parsed_toml)
