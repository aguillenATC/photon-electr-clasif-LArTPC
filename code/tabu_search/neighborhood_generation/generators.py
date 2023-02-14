from copy import deepcopy
from numbers import Number
from typing import Any
from ..base.solution import Solution
from ..value_ranges.ranges import NumericalRange, CategoricalRange
from .base import NeighborhoodGenerator

class FixedStepGenerator(NeighborhoodGenerator):

    def __init__(self, steps: Number):

        self.set_steps(steps)

    """For numerical variables, the step is the amount added or detracted from the original value
        to create two new neighbors"""
    """For categorical variables (specified as a list of possibilities), the step means the
        amount of different possibilities used to create new neighbors of the original one"""
    def set_steps(self, steps: Number) -> None:

        FixedStepGenerator.__check_dictionary_type(steps)
        FixedStepGenerator.__check_steps_format(steps)
        self.__steps = steps

    @staticmethod
    def __check_dictionary_type(steps: dict) -> None:

        if not isinstance(steps, dict):

            raise TypeError("Movement steps must be passed in a dictionary")

    @staticmethod
    def __check_steps_format(steps: dict) -> None:

        if not all([isinstance(step, Number) for step in steps.values()]):

            raise TypeError("Movement steps must be numerical")

    """Each neighbor generated differs from the original solution in the value
        of exactly one attribute; the rest stay unmodified"""
    def generate_neighborhood(self, generator) -> list[Solution]:

        neighbors = []
        s: Solution = self.trackers["progress"]["solution_history"].get_last()

        for attribute in s.attributes.keys():

            if isinstance(self._attr_ranges[attribute], NumericalRange):

                new_neighbors: list[Solution] = self.__generate_neighbors_of_numerical_attribute(s, attribute)
                neighbors.extend(new_neighbors)

            elif isinstance(self._attr_ranges[attribute], CategoricalRange):

                new_neighbors: list[Solution] = self.__generate_neighbors_of_categorical_attribute(s, attribute, generator)
                neighbors.extend(new_neighbors)

        return self.evaluators["fitness"].evaluate_batch(neighbors)

    def __generate_neighbors_of_numerical_attribute(self, s: Solution, attribute: str) -> list[Solution]:

        orig_value: Number = s.attributes[attribute]
        step_up, step_down = orig_value + self.__steps[attribute], orig_value - self.__steps[attribute]
        step_up_neighbor, step_down_neighbor = deepcopy(s), deepcopy(s)
        step_up_neighbor.attributes[attribute], step_down_neighbor.attributes[attribute] = step_up, step_down

        valid_neighbors = []

        if self.is_solution_valid(step_up_neighbor):

            valid_neighbors.append(step_up_neighbor)

        if self.is_solution_valid(step_down_neighbor):

            valid_neighbors.append(step_down_neighbor)

        return valid_neighbors

    def __generate_neighbors_of_categorical_attribute(self, s: Solution, attribute: str, generator) -> list[Solution]:

        orig_value: Any = s.attributes[attribute]
        chosen_values: Any = self._attr_ranges[attribute].random_values_without(orig_value, self.__steps[attribute], generator)

        valid_neighbors = []

        for new_value in chosen_values:

            new_neighbor: Solution = deepcopy(s)
            new_neighbor.attributes[attribute] = new_value

            if self.is_solution_valid(new_neighbor):

                valid_neighbors.append(new_neighbor)

        return valid_neighbors
