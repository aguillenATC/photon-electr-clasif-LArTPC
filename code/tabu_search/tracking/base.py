from abc import ABC, abstractmethod
from collections import deque
from typing import Any
import pandas as pd

"""Generic value tracker interface"""
class Tracker(ABC):

    def __init__(self, max_size = None):

        self._tracker = deque(maxlen = max_size)

    @abstractmethod
    def append(self) -> None:

        raise NotImplementedError

    def __getitem__(self, index: int):

        self._check_is_in_range(index)
        return self._tracker[index]

    def _check_is_in_range(self, index: int):

        if index >= self.size():

            raise IndexError("Tracker index out of range")

        elif index < 0 and abs(index) > self.size():

            raise IndexError("Tracker index out of range")

    def get_last(self) -> Any:

        if not self.empty():

            return self.__getitem__(-1)

        else:

            raise ValueError("Tracker is still empty")

    def empty(self) -> bool:

        return not len(self._tracker)

    def size(self) -> int:

        return len(self._tracker)

class SerializableTracker(Tracker):

    def __init__(self, max_size = None):

        super().__init__(max_size = max_size)
        self._df = pd.DataFrame()

    @abstractmethod
    def to_dataframe(self) -> pd.DataFrame:

        raise NotImplementedError
