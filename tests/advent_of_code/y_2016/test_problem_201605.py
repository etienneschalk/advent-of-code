import hashlib

import pytest


@pytest.mark.parametrize(
    "puzzle_input,expected", [("abc", "18f47a30"), ("abbhdwsy", "801b56a7")]
)
def test_problem_202205_part_1(puzzle_input: str, expected: str):
    found = 0
    i = 0
    letters = []
    while found != 8:
        hash = hashlib.md5((puzzle_input + str(i)).encode()).hexdigest()
        if hash.startswith("00000"):
            letters.append(hash[5])
            found += 1
            print(i)
        i += 1
    result = "".join(letters)
    assert result == expected


@pytest.mark.parametrize(
    "puzzle_input,expected", [("abc", "05ace8e3"), ("abbhdwsy", "424a0197")]
)
def test_problem_202205_part_2(puzzle_input: str, expected: str):
    found = 0
    i = 0
    letters = [" "] * 8
    while found != 8:
        hash = hashlib.md5((puzzle_input + str(i)).encode()).hexdigest()
        if hash.startswith("00000") and hash[5].isnumeric():
            index = int(hash[5])
            if (0 <= index < 8) and (letters[index] == " "):
                found += 1
                letters[index] = hash[6]
        i += 1
    result = "".join(letters)
    assert result == expected
