import pytest
from tabu_search.base.solution import Solution
from tabu_search.base.tabu_list import TabuList

def test_tabu_list_accepts_solutions():

    tabu_tenures = {"a": 2, "b": 2, "c": 2}
    tabu_list = TabuList(tabu_tenures)
    new_solution = Solution({"a": 10, "b": "something", "c": 3.14})
    was_not_in_tabu_list = new_solution not in tabu_list
    tabu_list.add_element(new_solution)
    is_now_in_tabu_list = new_solution in tabu_list

    assert was_not_in_tabu_list and is_now_in_tabu_list

@pytest.mark.parametrize("attributes, other_attributes, expected_result",
                         [({"a": 10, "b": "something", "c": 3.14}, {"a": 10, "b": "something", "c": 3.14}, True),
                          ({"a": 10, "b": "something", "c": 3.14}, {"a": 10, "b": "anything", "c": 4.13}, True),
                          ({"a": 10, "b": "something", "c": 3.14}, {"a": 20, "b": "anything", "c": 4.13}, False)])
def test_solution_is_in_tabu_list_if_any_of_its_values_are(attributes, other_attributes, expected_result):

    existing_solution = Solution(attributes)
    new_solution = Solution(other_attributes)
    tabu_tenures = {"a": 2, "b": 2, "c": 2}
    tabu_list = TabuList(tabu_tenures)
    tabu_list.add_element(existing_solution)

    assert (new_solution in tabu_list) == expected_result

@pytest.mark.parametrize("tabu_tenures",
                         [{"a": 0, "b": 0}, {"a": -1, "b": -1}, {"a": 2, "b": 0}])
def test_tabu_list_does_not_accept_invalid_tenures(tabu_tenures):

    with pytest.raises(ValueError):

        TabuList(tabu_tenures)

@pytest.mark.parametrize("attributes, tabu_tenures, iterations, should_contain",
                         [({"a": 42, "b": 3.14}, {"a": 2, "b": 3}, 2, True),
                          ({"a": 42, "b": 3.14}, {"a": 2, "b": 3}, 3, True),
                          ({"a": 42, "b": 3.14}, {"a": 2, "b": 3}, 4, False)])
def test_tabu_list_does_not_contain_solution_after_tenure_expires(attributes, tabu_tenures, iterations, should_contain):

    new_solution = Solution(attributes)
    tabu_list = TabuList(tabu_tenures)
    tabu_list.add_element(new_solution)

    for _ in range(iterations):

        tabu_list.update_tenures()

    assert (new_solution in tabu_list) == should_contain

def test_tabu_list_renews_tenure_if_existing_attributes_are_added():

    tenure = 2
    solution = Solution({"a": 42})
    tabu_tenures = {"a": tenure}
    tabu_list = TabuList(tabu_tenures)
    tabu_list.add_element(solution)

    for _ in range(tenure): # Next update after the loop should delete the solution if not renewed

        tabu_list.update_tenures()

    tabu_list.add_element(solution)
    tabu_list.update_tenures()

    assert solution in tabu_list
