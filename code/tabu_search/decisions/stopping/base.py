from abc import ABC, abstractmethod

"""Base class for search stopping criteria"""
class StoppingCriterion(ABC):

    @abstractmethod
    def should_stop(self) -> bool:

        raise NotImplementedError
