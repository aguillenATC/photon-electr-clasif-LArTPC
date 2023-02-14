from abc import ABC, abstractmethod
from ..base.range_user import AttributeRangeUser
from ..base.evaluator_user import EvaluatorUser
from ..base.tracker_user import TrackerUser

"""Base search initializer class"""
class SearchInitializer(AttributeRangeUser, EvaluatorUser, TrackerUser, ABC):

    """Creates the starting Solution for the tabu search procedure"""
    @abstractmethod
    def initialize_search(self) -> None:

        raise NotImplementedError
