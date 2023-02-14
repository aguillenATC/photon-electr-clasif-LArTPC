import os
from abc import ABC, abstractmethod
from ..base.tracker_user import TrackerUser
from ..tracking.base import Tracker

"""Base class for all kinds of post-execution result processing"""
class ResultProcessor(ABC, TrackerUser):

    def __init__(self, target_tracker: str):

        self.target: dict[str, str] = self._parse_target_tracker(target_tracker)

    @classmethod
    def set_results_path(cls, results_path: str) -> None:

        cls.results_path = results_path

    def check_and_create_folder_path(self, save_path: str) -> None:

        if not os.path.isdir(save_path):

            os.makedirs(save_path)

    def get_target_tracker(self) -> Tracker:

        return self.trackers[self.target["group"]][self.target["tracker"]]

"""Base class for post-execution operations on the results and/or gathered progress data"""
class PostProcessor(ResultProcessor):

    @abstractmethod
    def post_process(self) -> None:

        raise NotImplementedError

"""Base class for result storage functionality"""
class Writer(ResultProcessor):

    def __init__(self, save: dict, target_tracker: str):

        self.save_params = save
        super().__init__(target_tracker = target_tracker)

    @abstractmethod
    def write(self) -> None:

        raise NotImplementedError

    @classmethod
    def set_subfolder(cls, subfolder: str) -> None:

        cls.subfolder = subfolder

"""Base class for plot creators"""
class Plot(ResultProcessor):

    def __init__(self, plot: dict, save: dict, target_tracker: str):

        self.plot_params = plot
        self.save_params = save
        super().__init__(target_tracker = target_tracker)

    @abstractmethod
    def plot(self) -> None:

        raise NotImplementedError

    @classmethod
    def set_subfolder(cls, subfolder: str) -> None:

        cls.subfolder = subfolder

"""Base class for result file syncing with VCS, DB, etc."""
class Syncer(ResultProcessor):

    @abstractmethod
    def __init__(self):

        raise NotImplementedError

    @abstractmethod
    def sync(self) -> None:

        raise NotImplementedError
