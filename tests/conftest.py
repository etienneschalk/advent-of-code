import pytest

from advent_of_code.common.store import ExampleInputsStore


@pytest.fixture(scope="session")
def example_inputs() -> ExampleInputsStore:
    return ExampleInputsStore.from_private_toml()
