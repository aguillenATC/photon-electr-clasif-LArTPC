import pytest
from tabu_search.base.solution import Solution

def test_initialized_solution_is_not_reinitialized():

    s = Solution({})
    assert not s.get_reinitialization_flag()

def test_initialized_solution_is_not_evaluated():

    s = Solution({})
    assert not s.is_evaluated()

@pytest.mark.parametrize("attributes, other_attributes, expected_result",
                         [({"a": 10, "b": "something", "c": []}, {"a": 10, "b": "something", "c": []}, True),
                          ({"a": 20, "b": "something", "c": []}, {"a": 10, "b": "something", "c": []}, False)])
def test_solutions_are_equal_only_if_all_their_attributes_are(attributes, other_attributes, expected_result):

    s_1, s_2 = Solution(attributes), Solution(other_attributes)
    assert (s_1 == s_2) == expected_result

def test_solution_equality_is_not_affected_by_reinitialization_flag():

    s_1, s_2 = Solution({"a": 10, "b": "something", "c": []}), Solution({"a": 10, "b": "something", "c": []})
    s_1.set_reinitialization_flag = True
    s_2.set_reinitialization_flag = False
    assert s_1 == s_2

def test_solution_equality_is_not_affected_by_fitness():

    s_1, s_2 = Solution({"a": 10, "b": "something", "c": []}), Solution({"a": 10, "b": "something", "c": []})
    s_1.fitness, s_2.fitness = 1, 2
    assert s_1 == s_2

def test_evaluated_solution_is_greater_than_non_evaluated_solution():

    s_1, s_2 = Solution({}), Solution({})
    s_1.fitness = 42
    assert s_1 > s_2 and s_1 >= s_2
