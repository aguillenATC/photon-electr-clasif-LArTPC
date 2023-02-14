from abc import ABC, abstractmethod
from ..base.range_user import AttributeRangeUser
from ..base.evaluator_user import EvaluatorUser
from ..base.tracker_user import TrackerUser

"""Base search reinitializer class"""
class SearchReinitializer(AttributeRangeUser, EvaluatorUser, TrackerUser, ABC):

    """Creates another starting Solution for a restart in the tabu search
        procedure. Can be random, pre-determined, or based on some kind of
        search history"""
    @abstractmethod
    def reinitialize_search(self) -> None:

        raise NotImplementedError
