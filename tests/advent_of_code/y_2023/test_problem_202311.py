from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.y_2023.problem_202311 import (
    compute_proximity_matrix,
    compute_proximity_matrix_from_coord_array,
    compute_sum_of_shortest_paths_between_pairs,
    compute_sum_of_shortest_paths_part_2,
    create_chunk_coord_array,
    create_coord_array,
    expand_space,
    parse_text_input,
)


def test_problem_202311_part_1(example_inputs_2023: ExampleInputsStore):
    test_input = example_inputs_2023.retrieve(__file__)
    parsed_input = parse_text_input(test_input)

    test_expected_expanded = example_inputs_2023.retrieve(
        __file__, "EXAMPLE_EXPECTED_EXPANSION"
    )

    expected_expanded = parse_text_input(test_expected_expanded)

    expanded_space = expand_space(parsed_input)
    assert (expanded_space == expected_expanded).all()

    proximity_matrix = compute_proximity_matrix(expanded_space)
    assert proximity_matrix[5 - 1][9 - 1] == proximity_matrix[9 - 1][5 - 1] == 9
    assert proximity_matrix[1 - 1][7 - 1] == proximity_matrix[7 - 1][1 - 1] == 15
    assert proximity_matrix[3 - 1][6 - 1] == proximity_matrix[6 - 1][3 - 1] == 17
    assert proximity_matrix[8 - 1][9 - 1] == proximity_matrix[9 - 1][8 - 1] == 5

    actual_result = compute_sum_of_shortest_paths_between_pairs(proximity_matrix)
    assert actual_result == 374


def test_problem_202311_part_2(example_inputs_2023: ExampleInputsStore):
    test_input = example_inputs_2023.retrieve(__file__)
    parsed_input = parse_text_input(test_input)
    space_xda = parsed_input

    coord_array = create_coord_array(space_xda)

    chunk_coord_array = create_chunk_coord_array(space_xda, coord_array)

    # Source: pen and paper ^^
    expected_chunk_coord_array = coord_array.copy(
        data=[[0, 1], [0, 2], [0, 0], [1, 2], [1, 0], [1, 3], [2, 2], [2, 0], [2, 1]]
    )

    assert (chunk_coord_array == expected_chunk_coord_array).all()

    proximity_matrix_chunks = compute_proximity_matrix_from_coord_array(
        chunk_coord_array.compute()
    )

    # No need to expand space anymore
    proximity_matrix = compute_proximity_matrix(space_xda.compute())
    assert proximity_matrix[5 - 1][9 - 1] == proximity_matrix[9 - 1][5 - 1] == 9 - 2
    assert proximity_matrix[1 - 1][7 - 1] == proximity_matrix[7 - 1][1 - 1] == 15 - 3
    assert proximity_matrix[3 - 1][6 - 1] == proximity_matrix[6 - 1][3 - 1] == 17 - 4
    assert proximity_matrix[8 - 1][9 - 1] == proximity_matrix[9 - 1][8 - 1] == 5 - 1

    # Find back the result of part 1 where we added a space of 1
    expansion_coef = 1
    total_proximity = proximity_matrix + expansion_coef * proximity_matrix_chunks
    assert total_proximity[5 - 1][9 - 1] == total_proximity[9 - 1][5 - 1] == 9
    assert total_proximity[1 - 1][7 - 1] == total_proximity[7 - 1][1 - 1] == 15
    assert total_proximity[3 - 1][6 - 1] == total_proximity[6 - 1][3 - 1] == 17
    assert total_proximity[8 - 1][9 - 1] == total_proximity[9 - 1][8 - 1] == 5

    # Find back example results given in the problem description part 2
    # (don't forget to remove one: this is 1 * 10... but 9 added)
    expansion_coef = 10 - 1
    total_proximity = proximity_matrix + expansion_coef * proximity_matrix_chunks
    actual_result = compute_sum_of_shortest_paths_between_pairs(total_proximity)
    expected_result = 1030
    assert actual_result == expected_result
    assert (
        compute_sum_of_shortest_paths_part_2(space_xda, expansion_coef)
        == expected_result
    )

    expansion_coef = 100 - 1
    total_proximity = proximity_matrix + expansion_coef * proximity_matrix_chunks
    actual_result = compute_sum_of_shortest_paths_between_pairs(total_proximity)
    expected_result = 8410
    assert actual_result == expected_result
    assert (
        compute_sum_of_shortest_paths_part_2(space_xda, expansion_coef)
        == expected_result
    )
