# advent-of-code

## Development

### (:warning: Legacy) Template Files

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

### Pre-commit

To run all checks on the whole project:

```bash
pre-commit run --all
```

### Testing

Integration tests:

```bash
pytest --with-integration -k integration --durations=0
```

All tests : unit + integration tests. Slow tests are excluded.

```bash
poetry run pytest -v --with-integration --durations=0
```

Only slow tests, using multiple workers (requires `pytest-xdist`).

```bash
poetry run pytest -v --with-integration -m slow --durations=0 -n 4
```

Drawback: duration is displayed globally per worker, not for each individual test

Note: durations < 0.005 seem to be hidden. Use `-vv` to truly get all

```bash
poetry run pytest -vv --with-integration -m slow --durations=0 -n 4
```

See [Stack Overflow - Show durations of tests for pytest](https://stackoverflow.com/questions/27884404/printing-test-execution-times-and-pinning-down-slow-tests-with-py-test)

```bash
pytest --durations=0 # Show all times for tests and setup and teardown
pytest --durations=1 # Slowest test
pytest --durations=50 # Slowest 50 tests
```

## Experience Feedback

### Types of problems

Note: To get an overview of all input data types, grep for `type PuzzleInput =` globally in the project. It gives a quick overview over the variety of data structures used.
Scalar to Range manipulation, Sankey flow diagrams

- Day 5: If You Give A Seed A Fertilizer
  - Tags: Sankey, graph, mapping
  - The first problem on which I blocked. Visualizations on reddit helped
- Day 19: Aplenty
  - Tags: Sankey, graph, mapping, rules
  - Very similar to

recursion

graph shortest path

- Day 17: Clumsy Crucible
  - Tags: 2D-array, graph, dijkstra, shortest-path
  - This is Dijkstra with a custom State that supports consecutive moves constraints
- Day 23: A Long Walk
  - Tags: 2D-array, graph, shortest-path
  - The essence of the problem must be first extracted: walks can be represented as a graph
  - Then, find the shortest path inside this graph.
  - The first part is easier as the slopes make the graph a DAG
  - The second part includes cycles and must be bruteforce. The underlying graph is simple enough to enable smart bruteforcing.

Pure Simulation

- Day 22: Sand Slabs
  - Tags: 3D-array, graph
  - This problem is at first pure simulation. The simulation must be ran until the end. The final state is clear: all bricks must have fallen.
  - Not sure if there is a general solution that does not imply some simulation bruteforcing
  - This problem also embeds graph manipulation logic for part 2, but getting the simulation right was the most difficult.
- Day 16: The Floor Will Be Lava
  - Tags: 2D-array
  - Run the simulation until a stable end state is reached. We can assume the inputs are crafted specifically so that such an end-state does exist.
  - There is likely no "mathematical solution". So this problems leans at 100% dev, 0% math

Simulation for long enough then "smart pattern/cycle" to dramatically simplify the problem

- Day 8: Haunted Wasteland
  - Tags: graph, LCM
  - Input is a graph
  - Explosion of problem complexity in part 2
  - detect loops, then use lowest common multiple (LCM)
- Day 14: Parabolic Reflector Dish
  - Tags: 2D-array, simulation, cycle
  - A simulation of the tilting platform with moving rocks with obstacles must first be written
  - The input problem description requires an excessively huge simulation step count, fortunately a cycle emerges pretty soon, above which there is no point to continue running the simulation.
  - Part 2 is similar to Day 8
- Day 20: Pulse Propagation
  - Tags: simulation, graph, cycle, high-level-visualization-helps, rules
  - A simulation of an electronic circuit must first be written
  - Then, the essence of the problem must be extracted. Using graphviz to visualize the constructed graph resulting from the simulation setup is essential to get the big picture. Otherwise it is impossible to solve. It requires to find the pattern in the input
  - A cycle emerge, and then multiplying all the minimum-cycle for all branches helps reducing the simulation step count. This is like getting a low-frequency (high period) clock from several high-frequency (low period) ones combined with and AND gate. Note: if some periods are multiples between each other, the LCM applies
- Day 21: Step Counter
  - Tags: 2D-array, simulation, pattern, LCM, high-level-visualization-help
  - A simulation of the cellular automata must be ran for long enough
  - Then, the simulation becomes way too computational heavy, with an explosion of the size of the input data (becoming orders of magnitude larger, with `O(n**2)`)
  - The space becomes infinite, tiling the original finite provided input data

Pure Visualization

- Day 25: Snowverload
  - Tags: graph, high-level-visualization-help
  - Using graphviz to visualize the graph is a way to identify clusters in this "clustering graph". Graphviz already contains logic to smartly place nodes relatively to each others.
- Pure Math

- Day 24: Never Tell Me The Odds
  - Require solving a linear system of equation. The use of external tools seems mandatory, eg using `sympy` for symbolic mathematics. It is used to solve the system of equations.
  - This is one of the rare problems that are more "float-oriented", and not "int-oriented". Getting precise exact numbers from a simulation is hard. Hence pure math helping here.

## Documentation

```bash
cd docs
# sphinx-autobuild source _build/html
poetry run sphinx-build -E source _build/html # clear cache
poetry run sphinx-autobuild source _build/html # autobuild
# sphinx-autobuild -E source _build/html # clear cache (not advised with autobuild)
```
