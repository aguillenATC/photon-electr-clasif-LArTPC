from ..base.solution import Solution
from .base import NeighborSelector
from ..base.tracker_user import TrackerUser

class TabuIfBestSelector(NeighborSelector, TrackerUser):

    def select_next_solution(self, neighborhood: list[Solution]) -> None:

        best_neighbor = Solution({})
        best_tabu_neighbor = Solution({})

        for neighbor in neighborhood:

            if neighbor in self.tabu_list:

                if best_tabu_neighbor < neighbor:

                    best_tabu_neighbor = neighbor

            else:

                if best_neighbor < neighbor:

                    best_neighbor = neighbor

        best_solution_so_far: Solution = self.trackers["progress"]["best_solution_history"].get_last()

        if best_tabu_neighbor > best_neighbor and best_tabu_neighbor > best_solution_so_far:

            next_solution = best_tabu_neighbor

        elif not best_neighbor.is_evaluated():

            next_solution: Solution = best_tabu_neighbor

        else:

            next_solution: Solution = best_neighbor

        self.tabu_list.add_element(next_solution)
        self.tabu_list.update_tenures()
        self.update_tracker_group("progress", next_solution)
