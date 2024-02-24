import pytest

from advent_of_code.common.store import ExampleInputsStore, ExpectedAnswersStore


@pytest.fixture(scope="session")
def example_inputs() -> ExampleInputsStore:
    return ExampleInputsStore.from_private_resources_repository()


@pytest.fixture(scope="session")
def expected_answers() -> ExpectedAnswersStore:
    return ExpectedAnswersStore.from_private_resources_repository()
