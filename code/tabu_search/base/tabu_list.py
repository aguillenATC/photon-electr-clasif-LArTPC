"""Tabu list base class"""
from typing import Any
from .solution import Solution


class TabuList:

    """Contains separate tabu lists for every different attribute of a Solution"""
    def __init__(self, attributes_and_tenures: dict[str, int]):

        self.__check_all_tenures_are_positive_and_nonzero(attributes_and_tenures)
        self.tabu_dicts: dict[str, dict[Any, int]] = {name: {} for name in attributes_and_tenures.keys()}
        self.tenures: dict[str, int] = attributes_and_tenures.copy()

    def __check_all_tenures_are_positive_and_nonzero(self, tenures: dict[str, int]):

        for tenure in tenures.values():

            if tenure <= 0:

                raise ValueError("Attribute tenures must be positive and non-zero")

    """Determines whether any attribute values contained in a Solution instance
        are currently tabu"""
    def __contains__(self, s: Solution) -> bool:

        return any([value in self.tabu_dicts[attr].keys()
                    for attr, value in s.attributes.items()])

    """Adds the attribute values of a Solution instance to the tabu lists
        (or resets their tabu status if the Solution instance had tabu attributes
        but was used anyway)"""
    def add_element(self, s: Solution) -> None:

        for key, val in s.attributes.items():

            self.tabu_dicts[key][val] = self.tenures[key]

    """Advances one iteration in the countdown of every current tabu element's
        permanence in the tabu list. After an element reaches 0 iterations
        left, it is removed"""
    def update_tenures(self) -> None:

        for tabu_dict in self.tabu_dicts.values():

            for key, val in list(tabu_dict.items()):

                if val > 0:

                    tabu_dict[key] = val - 1

                else:

                    tabu_dict.pop(key, None)
