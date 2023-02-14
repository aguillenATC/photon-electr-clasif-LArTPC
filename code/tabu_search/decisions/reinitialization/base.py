from abc import ABC, abstractmethod

"""Base class for search reinitialization criteria"""
class ReinitializationCriterion(ABC):

    @abstractmethod
    def should_reinitialize(self) -> bool:

        raise NotImplementedError
