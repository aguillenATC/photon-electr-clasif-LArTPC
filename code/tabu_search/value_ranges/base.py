from abc import ABC, abstractmethod

"""Base class to encapsulate all the possible values a
    given attribute could take"""
class ValueRange(ABC):

    """Stores the representation of the range (e.g. a tuple with
        minimum and maximum values, or a list of possibilities)"""
    @abstractmethod
    def __init__(self):

        raise NotImplementedError

    """Checks whether a value is contained within the stored range"""
    @abstractmethod
    def __contains__(self, value) -> bool:

        raise NotImplementedError

    """Utility to return a random value contained within the stored range"""
    @abstractmethod
    def random_value(self, seed):

        raise NotImplementedError
