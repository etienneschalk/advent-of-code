from dataclasses import asdict
from advent_of_code.common import save_txt
from advent_of_code.year_2023.year_2023_day_19 import (
    construct_initial_part_range,
    parse_text_input,
    visu_recur_dict_part_2,
)

EXAMPLE_INPUT = """

px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}

"""


def test_year_2023_day_19_part_1():
    test_input = EXAMPLE_INPUT
    parsed_input = parse_text_input(test_input)
    assert parsed_input.apply_to_all() == list("ARARA")
    solve_1 = parsed_input.solve_part_1()
    assert solve_1 == {0: 7540, 2: 4623, 4: 6951}
    assert sum(solve_1.values()) == 19114
    ...


def test_year_2023_day_19_part_2():
    test_input = EXAMPLE_INPUT
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
