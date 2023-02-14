import pandas as pd
from numpy import array
from math import inf
from .base import Tracker, SerializableTracker
from ..base.solution import Solution

class FitnessHistoryTracker(SerializableTracker):

    def __init__(self, max_size = None):

        super().__init__(max_size = max_size)

    def append(self, solution: Solution) -> None:

        self._tracker.append(solution.fitness)

    def to_dataframe(self) -> pd.DataFrame:

        if self._df.empty and not self.empty():

            self._df = pd.DataFrame(self.to_array(), columns = ["fitness"])

        return self._df

    def to_array(self) -> array:

        return array(self._tracker)

    def variation_last_n(self, n: int):

        if n > self.size():

            return inf

        else:

            return self.get_last() - self._tracker[-n]

class SolutionHistoryTracker(SerializableTracker):

    def __init__(self, max_size = None):

        super().__init__(max_size = max_size)
        self.step: int = 0

    def append(self, solution: Solution) -> None:

        self._tracker.append({**solution.attributes,
                                "fitness": solution.fitness,
                                "reinitialized": solution.get_reinitialization_flag()})
        self.step += 1

    def __getitem__(self, index: int) -> Solution:

        self._check_is_in_range(index)
        s = Solution({key: value for key, value in self._tracker[index].items()
                                    if key not in ["fitness", "reinitialized"]})
        s.fitness = self._tracker[index]["fitness"]
        return s

    def get_step_count(self) -> int:

        return self.step

    def to_dataframe(self) -> pd.DataFrame:

        if self._df.empty and not self.empty():

            deque_as_list = list(self._tracker)
            self._df = pd.DataFrame(deque_as_list)

        return self._df

class BestFitnessTracker(SerializableTracker):

    def __init__(self, max_size = None):

        super().__init__(max_size = max_size)

    def append(self, solution: Solution) -> None:

        if self.empty() or self.get_last() < solution.fitness:

            self._tracker.append(solution.fitness)

    def to_dataframe(self) -> pd.DataFrame:

        if self._df.empty and not self.empty():

            self._df = pd.DataFrame(self.to_array(), columns = ["fitness"])

        return self._df

    def to_array(self) -> array:

        return array(self._tracker)

class BestSolutionTracker(SerializableTracker):

    def __init__(self, max_size = None):

        super().__init__(max_size = max_size)

    def append(self, solution: Solution) -> None:

        if self.empty() or self.get_last() < solution:

            self._tracker.append({**solution.attributes,
                                    "fitness": solution.fitness})

    def __getitem__(self, index: int) -> Solution:

        self._check_is_in_range(index)
        s = Solution({key: value for key, value in self._tracker[index].items()
                                    if not key == "fitness"})
        s.fitness = self._tracker[index]["fitness"]
        return s

    def to_dataframe(self) -> pd.DataFrame:

        if self._df.empty and not self.empty():

            deque_as_list = list(self._tracker)
            self._df = pd.DataFrame(deque_as_list)

        return self._df

class ModelTracker(Tracker):

    def __init__(self, max_size = 1):

        super().__init__(max_size = max_size)

    def append(self, model) -> None:

        self._tracker.append(model)

class TimeTracker(SerializableTracker):

    def __init__(self, max_size = 1):

        super().__init__(max_size = max_size)

    def append(self, time: float) -> None:

        self._tracker.append(time)

    def to_dataframe(self) -> pd.DataFrame:

        if self._df.empty and not self.empty():

            self._df = pd.DataFrame(self.to_array(), columns = ["time"])

        return self._df

    def to_array(self) -> array:

        return array(self._tracker)

class InstantaneousPowerTracker(SerializableTracker):

    def __init__(self):

        super().__init__(max_size = None)

    def append(self, measurement: dict[str, float]) -> None:

        self._tracker.append({**measurement})

    def to_dataframe(self) -> pd.DataFrame:

        if self._df.empty and not self.empty():

            deque_as_list = list(self._tracker)
            self._df = pd.DataFrame(deque_as_list)

        return self._df

class AccumulatedEnergyTracker(SerializableTracker):

    def __init__(self):

        super().__init__(max_size = 1)

    def append(self, measurement: dict[str, float]) -> None:

        self._tracker.append({**measurement})

    def to_dataframe(self) -> pd.DataFrame:

        if self._df.empty and not self.empty():

            deque_as_list = list(self._tracker)
            self._df = pd.DataFrame(deque_as_list)

        return self._df
