from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.year_2023.problem_202319 import (
    construct_initial_part_range,
    parse_text_input,
)


def test_problem_202319_part_1(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    parsed_input = parse_text_input(test_input)
    assert parsed_input.apply_to_all() == list("ARARA")
    solve_1 = parsed_input.solve_part_1()
    assert solve_1 == {0: 7540, 2: 4623, 4: 6951}
    assert sum(solve_1.values()) == 19114
    ...


def test_problem_202319_part_2(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    parsed_input = parse_text_input(test_input)
    initial_part_range = construct_initial_part_range()
    solve_2 = parsed_input.apply_to_range(initial_part_range)
    assert solve_2.mapping["qqz"][0].volume() == 169600e9
    assert solve_2.mapping["px"][0].volume() == 86400e9
    assert solve_2.children["qqz"][0].mapping["qs"][0].volume() == 78720e9
    assert (
        solve_2.children["qqz"][0].children["qs"][0].mapping["lnx"][0].volume()
        == 43392e9
    )
    assert solve_2.children["qqz"][0].mapping["hdj"][0].volume() == 40896e9
    assert solve_2.children["px"][0].mapping["qkq"][0].volume() == 43308e9
    assert (
        solve_2.children["px"][0].children["qkq"][0].mapping["crn"][0].volume()
        == 27987795e6
    )

    assert solve_2.children["px"][0].mapping["rfg"][0].volume() == 22515570e6
    assert (
        solve_2.children["qqz"][0].children["hdj"][0].mapping["pv"][0].volume()
        == 19039360e6
    )
    assert (
        solve_2.children["px"][0].children["rfg"][0].mapping["gd"][0].volume()
        == 8939515200000
    )

    assert parsed_input.solve_part_2(initial_part_range) == 167409079868000

    # Bug fixed: because of dict key overwrite!
    # np.sum(np.array([np.prod([r.stop - r.start + 1 for r in asdict(a).values()]) for a in acc]))  / 167409079868000

    # 0.55
    # np.sum(np.array([np.prod([r.stop - r.start + 1 for r in asdict(a).values()]) for a in acc])) / 4000**4

    # 0.33
    # np.sum(np.array([np.prod([r.stop - r.start + 1 for r in asdict(a).values()]) for a in rej])) / 4000**4

    # acc + rej != 4000***4
    # assert 167409079868000 == None
    ...
