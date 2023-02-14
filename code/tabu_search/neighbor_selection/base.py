from abc import ABC, abstractmethod
from ..base.tabu_list import TabuList
from ..base.tracker_user import TrackerUser

"""Base neighbor selector class"""
class NeighborSelector(TrackerUser, ABC):

    def __init__(self, tabu_list: TabuList):

        self.__check_is_tabulist(tabu_list)
        self.tabu_list = tabu_list

    @staticmethod
    def __check_is_tabulist(tabu_list: TabuList) -> None:

        if not isinstance(tabu_list, TabuList):

            raise TypeError("Tabu list must be of type TabuList")

    """Chooses the next solution from a batch of already-evaluated solutions"""
    @abstractmethod
    def select_next_solution(self, neighborhood) -> None:

        raise NotImplementedError
