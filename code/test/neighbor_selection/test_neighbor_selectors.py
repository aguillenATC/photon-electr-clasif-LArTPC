import pytest
from tabu_search.base.solution import Solution
from tabu_search.neighbor_selection.selectors import TabuIfBestSelector
from tabu_search.base.tabu_list import TabuList
from tabu_search.base.tracker_user import TrackerUser
from tabu_search.tracking.trackers import BestSolutionTracker, SolutionHistoryTracker

@pytest.mark.parametrize("previous_best_fitness, tabu_fitness, non_tabu_fitness, should_choose_tabu",
                         [(10, 30, 20, True),
                          (10, 20, 30, False),
                          (10, 30, 30, False),
                          (40, 30, 20, False)])
def test_select_tabu_neighbor_only_if_overall_best(previous_best_fitness, tabu_fitness, non_tabu_fitness, should_choose_tabu):

    # Setup the trackers that will interact with the selector
    regular_tracker, best_solution_tracker = SolutionHistoryTracker(), BestSolutionTracker()
    TrackerUser.set_tracker_group("progress", {"solution_history": regular_tracker,
                                               "best_solution_history": best_solution_tracker})

    previous_best, tabu, non_tabu = Solution({"a": 1}), Solution({"a": 2}), Solution({"a": 3})
    previous_best.fitness, tabu.fitness, non_tabu.fitness = previous_best_fitness, tabu_fitness, non_tabu_fitness

    tabu_tenures = {"a": 50}
    tabu_list = TabuList(tabu_tenures)
    tabu_list.add_element(tabu) # The tabu solution must have already been added to the tabu list prior to the test
    neighbor_selector = TabuIfBestSelector(tabu_list)

    TrackerUser.update_tracker_group("progress", previous_best) # Simulate search initialization by adding the first solution
    neighbor_selector.select_next_solution([tabu, non_tabu])

    assert (TrackerUser.trackers["progress"]["solution_history"].get_last() == tabu) == should_choose_tabu
