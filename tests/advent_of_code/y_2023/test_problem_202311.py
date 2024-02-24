from advent_of_code.common.store import ExampleInputsStore
from advent_of_code.y_2023.problem_202311 import (
    compute_adjacency_matrix,
    compute_adjacency_matrix_from_coord_array,
    compute_sum_of_shortest_paths_between_pairs,
    compute_sum_of_shortest_paths_part_2,
    create_chunk_coord_array,
    create_coord_array,
    expand_space,
    parse_text_input,
)


def test_problem_202311_part_1(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    parsed_input = parse_text_input(test_input)

    test_expected_expanded = example_inputs.retrieve(
        __file__, "EXAMPLE_EXPECTED_EXPANSION"
    )

    expected_expanded = parse_text_input(test_expected_expanded)

    expanded_space = expand_space(parsed_input)
    assert (expanded_space == expected_expanded).all()

    adjacency_matrix = compute_adjacency_matrix(expanded_space)
    assert adjacency_matrix[5 - 1][9 - 1] == adjacency_matrix[9 - 1][5 - 1] == 9
    assert adjacency_matrix[1 - 1][7 - 1] == adjacency_matrix[7 - 1][1 - 1] == 15
    assert adjacency_matrix[3 - 1][6 - 1] == adjacency_matrix[6 - 1][3 - 1] == 17
    assert adjacency_matrix[8 - 1][9 - 1] == adjacency_matrix[9 - 1][8 - 1] == 5

    actual_result = compute_sum_of_shortest_paths_between_pairs(adjacency_matrix)
    assert actual_result == 374


def test_problem_202311_part_2(example_inputs: ExampleInputsStore):
    test_input = example_inputs.retrieve(__file__)
    parsed_input = parse_text_input(test_input)
    space_xda = parsed_input

    coord_array = create_coord_array(space_xda)

    chunk_coord_array = create_chunk_coord_array(space_xda, coord_array)

    # Source: pen and paper ^^
    expected_chunk_coord_array = coord_array.copy(
        data=[[0, 1], [0, 2], [0, 0], [1, 2], [1, 0], [1, 3], [2, 2], [2, 0], [2, 1]]
    )

    assert (chunk_coord_array == expected_chunk_coord_array).all()

    adjacency_matrix_chunks = compute_adjacency_matrix_from_coord_array(
        chunk_coord_array.compute()
    )

    # No need to expand space anymore
    adjacency_matrix = compute_adjacency_matrix(space_xda.compute())
    assert adjacency_matrix[5 - 1][9 - 1] == adjacency_matrix[9 - 1][5 - 1] == 9 - 2
    assert adjacency_matrix[1 - 1][7 - 1] == adjacency_matrix[7 - 1][1 - 1] == 15 - 3
    assert adjacency_matrix[3 - 1][6 - 1] == adjacency_matrix[6 - 1][3 - 1] == 17 - 4
    assert adjacency_matrix[8 - 1][9 - 1] == adjacency_matrix[9 - 1][8 - 1] == 5 - 1

    # Find back the result of part 1 where we added a space of 1
    expansion_coef = 1
    total_adjacency = adjacency_matrix + expansion_coef * adjacency_matrix_chunks
    assert total_adjacency[5 - 1][9 - 1] == total_adjacency[9 - 1][5 - 1] == 9
    assert total_adjacency[1 - 1][7 - 1] == total_adjacency[7 - 1][1 - 1] == 15
    assert total_adjacency[3 - 1][6 - 1] == total_adjacency[6 - 1][3 - 1] == 17
    assert total_adjacency[8 - 1][9 - 1] == total_adjacency[9 - 1][8 - 1] == 5

    # Find back example results given in the problem description part 2
    # (don't forget to remove one: this is 1 * 10... but 9 added)
    expansion_coef = 10 - 1
    total_adjacency = adjacency_matrix + expansion_coef * adjacency_matrix_chunks
    actual_result = compute_sum_of_shortest_paths_between_pairs(total_adjacency)
    expected_result = 1030
    assert actual_result == expected_result
    assert (
        compute_sum_of_shortest_paths_part_2(space_xda, expansion_coef)
        == expected_result
    )

    expansion_coef = 100 - 1
    total_adjacency = adjacency_matrix + expansion_coef * adjacency_matrix_chunks
    actual_result = compute_sum_of_shortest_paths_between_pairs(total_adjacency)
    expected_result = 8410
    assert actual_result == expected_result
    assert (
        compute_sum_of_shortest_paths_part_2(space_xda, expansion_coef)
        == expected_result
    )
