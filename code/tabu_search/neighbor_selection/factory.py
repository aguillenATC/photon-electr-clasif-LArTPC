from .base import NeighborSelector
from .selectors import TabuIfBestSelector

class NeighborSelectorFactory():

    neighbor_selector_mapping = {"tabu_if_best_overall": TabuIfBestSelector}

    @classmethod
    def create_neighbor_selector(cls, type, parameters = {}) -> NeighborSelector:

        return cls.neighbor_selector_mapping[type](**parameters)
