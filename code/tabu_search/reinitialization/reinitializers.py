from ..base.solution import Solution
from .base import SearchReinitializer

class RandomReinitializer(SearchReinitializer):

    def reinitialize_search(self, generator) -> None:

        attributes = {attribute: range_object.random_value(generator)
                        for attribute, range_object in self._attr_ranges.items()}

        evaluated_solution: Solution = self.evaluators["fitness"].evaluate(Solution(attributes))
        evaluated_solution.set_reinitialization_flag()
        self.update_tracker_group("progress", evaluated_solution)
