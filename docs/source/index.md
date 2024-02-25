---
hide-toc: true
---

# Advent of Blog

Welcome to this blog!

I try to describe my solutions and struggles that I encountered during the Advent of Code challenge of 2023.

The final goal is to achieve a true multimedia journal with videos, interactive notebooks as well as a comprehensive documentation of the code.

Goals are multiples. They are not achieved at the time of writing, but are written here to set the bar the highest possible.

- Problem-solving sharpening
  - Go beyond the "one-off" Advent of Code problem resolution and build a consistent framework aiming at easing the resolution of future problems, making them documented and reproducible
  - Consolidate my own comprehension of problems ; I won't hide that I more than often got inspiration from the [Advent of Code Reddit forum](https://www.reddit.com/r/adventofcode/)
- Technical improvement
  - Experiment with latest Python features, tools and good practices with full liberty
  - Use this project as a pool of knowledge for potential future usages
- Work on communication
  - How to explain the reasoning behind the solutions of Advent of Code to both a technical and non-technical audience
  - How to provide helpful visualizations of problems

## Experience Feedback

### Types of problems

Focused on Year 2023.

```{caution}
The following classification is subjective.
```

```{tip}
To get an overview of all input data types, grep for `type PuzzleInput =` globally in the project. It gives a quick overview over the variety of data structures used.
Scalar to Range manipulation, Sankey flow diagrams
```

#### Summary

| Day   | Category |
| ----- | -------- |
| `d01` | PO       |
| `d02` | GS       |
| `d03` | PO       |
| `d04` | GS       |
| `d05` | SD       |
| `d06` | PM       |
| `d07` | GS       |
| `d08` | SWC      |
| `d09` | MT       |
| `d10` | VPS      |
| `d11` | MT       |
| `d12` | PS       |
| `d13` | PS       |
| `d14` | SWC      |
| `d15` | PS       |
| `d16` | PS       |
| `d17` | GSP      |
| `d18` | MT       |
| `d19` | SD       |
| `d20` | SWC      |
| `d21` | SWC      |
| `d22` | PS       |
| `d23` | GSP      |
| `d24` | PM       |
| `d25` | PV       |

#### Parsing Oriented

- **Day 01**: Trebuchet
  - Tags: parsing
  - The main difficulty is parsing properly the input, and taking into account an edge can that can otherwise turn out to be fatal
- **Day 03**: Gear Ratios
  - Tags: parsing
  - The main difficulty is parsing and exploiting the input, especially at the beginning of the challenge
  - My resulting code is overcomplicated, at the exact opposite of the "Pure Math" problems. It is not Python friendly as it involves writing "low-level" code with intensive for loops

#### Game Simulation

- **Day 02**: Cube Conundrum
  - Tags: game
- **Day 04**: Scratchcards
  - Tags: game, cards
- **Day 07**: Camel Cards
  - Tags: game, cards
  - Playing an altered version of Poker

#### Sankey Diagram

- **Day 05**: If You Give A Seed A Fertilizer
  - Tags: Sankey, graph, mapping
  - The first problem on which I blocked. Visualizations on reddit helped
- **Day 19**: Aplenty
  - Tags: Sankey, graph, mapping, rules
  - Very similar to day 5

#### Algorithmic Problem

- **Day 12**: Hot Springs
  - Tags: nonogram
  - I fell into the recursion and memoization pitfall, that does not scale at all
  - An elegant solution exists involving no recursion nor memoization, but I adapted a solution from reddit. I need to dig more into the theory behind it.
  - Using a state allows to reduce the number of inputs (the essence of a state), limiting history but allowing solving the part 2 in reasonable time!
  - Best solution I found on Reddit: https://www.reddit.com/r/adventofcode/comments/18hbjdi/comment/kd5jucy/

#### Graph Shortest Path

- **Day 17**: Clumsy Crucible
  - Tags: 2D-array, graph, dijkstra, shortest-path
  - This is Dijkstra with a custom State that supports consecutive moves constraints
- **Day 23**: A Long Walk
  - Tags: 2D-array, graph, shortest-path
  - The essence of the problem must be first extracted: walks can be represented as a graph
  - Then, find the shortest path inside this graph.
  - The first part is easier as the slopes make the graph a DAG
  - The second part includes cycles and must be bruteforce. The underlying graph is simple enough to enable smart bruteforcing.

#### Pure Simulation

- **Day 22**: Sand Slabs
  - Tags: 3D-array, graph
  - This problem is at first pure simulation. The simulation must be ran until the end. The final state is clear: all bricks must have fallen.
  - Not sure if there is a general solution that does not imply some simulation bruteforcing
  - This problem also embeds graph manipulation logic for part 2, but getting the simulation right was the most difficult.
- **Day 16**: The Floor Will Be Lava
  - Tags: 2D-array, recursion
  - Run the simulation until a stable end state is reached. We can assume the inputs are crafted specifically so that such an end-state does exist.
  - There is likely no "mathematical solution". So this problems leans at 100% dev, 0% math
- **Day 15**: Lens Library
  - Tags: instructions
  - Parse the list of instructions and run the simulation
  - Same vibe as the beam simulator (Day 16), but way simpler
- **Day 13**: Point of Incidence
  - Tags: 2D-array
  - The part 2 is about finding the "simple trick" to adapt with almost no code change the logic from part 1. Once found it seems obvious, but it is not obvious to find at first when following a pure "coding" approach.

#### Simulation With Cycle

Run the simulation for long enough then "smart pattern/cycle" to dramatically simplify the problem

- **Day 08**: Haunted Wasteland
  - Tags: graph, LCM
  - Input is a graph
  - Explosion of problem complexity in part 2
  - detect loops, then use lowest common multiple (LCM)
- **Day 14**: Parabolic Reflector Dish
  - Tags: 2D-array, simulation, cycle
  - A simulation of the tilting platform with moving rocks with obstacles must first be written
  - The input problem description requires an excessively huge simulation step count, fortunately a cycle emerges pretty soon, above which there is no point to continue running the simulation.
  - Part 2 is similar to Day 8
- **Day 20**: Pulse Propagation
  - Tags: simulation, graph, cycle, high-level-visualization-helps, rules
  - A simulation of an electronic circuit must first be written
  - Then, the essence of the problem must be extracted. Using graphviz to visualize the constructed graph resulting from the simulation setup is essential to get the big picture. Otherwise it is impossible to solve. It requires to find the pattern in the input
  - A cycle emerges, and then multiplying all the minimum-cycle for all branches helps reducing the simulation step count. This is like getting a low-frequency (high period) clock from several high-frequency (low period) ones combined with and AND gate. Note: if some periods are multiples between each other, the LCM applies
- **Day 21**: Step Counter
  - Tags: 2D-array, simulation, pattern, LCM, high-level-visualization-help
  - A simulation of the cellular automata must be ran for long enough
  - Then, the simulation becomes way too computational heavy, with an explosion of the size of the input data (becoming orders of magnitude larger, with `O(n**2)`)
  - The space becomes infinite, tiling the original finite provided input data

#### Visual Problem Solving

- **Day 10**: Pipe Maze
  - tags: 2D-Array
  - This problem does require using some image-processing algorithm, but to solve it, a visual intuition helps a lot.
  - It can be solved at "high-level" by knowing which tool to use (even an image editor does the job!) rather than knowing how to implement the tool. In that case, the tool to use is [Flood Fill](https://en.wikipedia.org/wiki/Flood_fill)

#### Pure Visualization

- **Day 25**: Snowverload
  - Tags: graph, high-level-visualization-help
  - Using graphviz to visualize the graph is a way to identify clusters in this "clustering graph". Graphviz already contains logic to smartly place nodes relatively to each others.
  - This can be solved humanely without the need for an algorithm, thanks to the work already made by graphviz, hence the categorization in "pure visualization" even if it could be probably solved more formally.

#### Pure Math

- **Day 24**: Never Tell Me The Odds
  - Tags: symbolic-mathematics
  - Require solving a linear system of equation. The use of external tools seems mandatory, eg using `sympy` for symbolic mathematics. It is used to solve the system of equations.
  - This is one of the rare problems that are more "float-oriented", and not "int-oriented". Getting precise exact numbers from a simulation is hard. Hence pure math helping here.
- **Day 06**:
  - Tags: formula
  - The problem requires solving quadratic equations
  - Beware of the floats...

#### Math Tendency

- **Day 18**
  - Tags: polygon, area
  - The problem is to compute the area of a large polygon
  - The coding part is limited to translating the mathematical formulae into Python code.
- **Day 11**: Cosmic Expansion
  - Tags: 2D-array, graph, adjacency-matrix, chunks
  - This problem deserves its place in the "Pure Math" category as the step from step 1 to step 2 is generalizing a formula, and applying the same function but with different arguments.
  - Trying the bruteforce approach is pointless
- **Day 09**: Mirage Maintenance
  - tags: finite-difference
  - [`np.roll`](https://numpy.org/doc/stable/reference/generated/numpy.roll.html) is your friend
  - Solving part 2 involves reusing the same function as in part 1 but with a different argument

```{toctree}
:caption:
:hidden:

readme_link
```

```{toctree}
:caption:
:hidden:

videos/index
```

```{toctree}
:caption:
:hidden:

notebooks/index
```

```{toctree}
:caption:
:hidden:

autoapi/index
```
