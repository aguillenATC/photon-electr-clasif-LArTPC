from abc import ABC, abstractmethod
from ..base.range_user import AttributeRangeUser
from ..base.evaluator_user import EvaluatorUser
from ..base.solution import Solution
from ..base.tracker_user import TrackerUser

"""Base neighborhood generator class"""
class NeighborhoodGenerator(AttributeRangeUser, EvaluatorUser, TrackerUser, ABC):

    """Generates the neighbors of a given Solution according to the allowed
        parameter ranges and movements in the search space"""
    @abstractmethod
    def generate_neighborhood(self, s) -> list[Solution]:

        raise NotImplementedError
