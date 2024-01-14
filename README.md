# advent-of-code

## Development

Start development for a given day and year by generating template files:

```bash
python advent_of_code/jobs/code_generation.py --year 2022 --day 5
```

```txt
Started Generation
Generating puzzle_input
    Written puzzle_input to resources/advent_of_code/year_2022/input_year_2022_day_05.txt
Generating source_code
    Written source_code to advent_of_code/year_2022/year_2022_day_05.py
Generating test_code
    Written test_code to tests/advent_of_code/year_2022/test_year_2022_day_05.py
Finished Generation
```

### Testing

All tests : integration tests + slow tests

```bash
poetry run pytest -v --with-integration -m slow
```

See https://stackoverflow.com/questions/27884404/printing-test-execution-times-and-pinning-down-slow-tests-with-py-test

```bash
pytest --durations=0 # Show all times for tests and setup and teardown
pytest --durations=1 # Slowest test
pytest --durations=50 # Slowest 50 tests
```
