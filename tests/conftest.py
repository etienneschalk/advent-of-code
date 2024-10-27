import pytest

from advent_of_code.common.store import ExampleInputsStore, ExpectedAnswersStore


@pytest.fixture(scope="session")
def example_inputs_2016() -> ExampleInputsStore:
    return ExampleInputsStore.from_private_resources_repository(2016)


@pytest.fixture(scope="session")
def example_inputs_2019() -> ExampleInputsStore:
    return ExampleInputsStore.from_private_resources_repository(2019)


@pytest.fixture(scope="session")
def example_inputs_2022() -> ExampleInputsStore:
    return ExampleInputsStore.from_private_resources_repository(2022)


@pytest.fixture(scope="session")
def example_inputs_2023() -> ExampleInputsStore:
    return ExampleInputsStore.from_private_resources_repository(2023)


@pytest.fixture(scope="session")
def expected_answers_2016() -> ExpectedAnswersStore:
    return ExpectedAnswersStore.from_private_resources_repository(2016)


@pytest.fixture(scope="session")
def expected_answers_2022() -> ExpectedAnswersStore:
    return ExpectedAnswersStore.from_private_resources_repository(2022)


@pytest.fixture(scope="session")
def expected_answers_2023() -> ExpectedAnswersStore:
    return ExpectedAnswersStore.from_private_resources_repository(2023)
