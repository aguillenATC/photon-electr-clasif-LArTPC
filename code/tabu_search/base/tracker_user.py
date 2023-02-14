from typing import Iterable
from .solution import Solution
from ..tracking.base import Tracker
from ..tracking.factory import TrackerFactory

"""Base class to give components the ability to access search trackers"""
class TrackerUser:

    trackers: dict[str, dict[str, Tracker]] = {}

    @classmethod
    def create_tracker(cls, tracker_group: str, tracker_name: str, type: str, parameters = {}) -> None:

        if tracker_group not in cls.trackers:

            cls.create_tracker_group(tracker_group)

        cls.trackers[tracker_group][tracker_name] = TrackerFactory.create_tracker(type, **parameters)

    @classmethod
    def create_tracker_group(cls, tracker_group: str) -> None:

        cls.trackers[tracker_group] = {}

    @classmethod
    def add_tracker_to_group(cls, tracker_group: str, tracker_name: str, tracker_object: Tracker) -> None:

        cls.__check_is_tracker(tracker_object)
        cls.trackers[tracker_group][tracker_name] = tracker_object

    @classmethod
    def set_tracker_group(cls, tracker_group: str, tracker_container: dict) -> None:

        cls.__check_all_objects_are_trackers(tracker_container.values())
        cls.trackers[tracker_group] = tracker_container

    @classmethod
    def update_tracker(cls, tracker_group: str, tracker_name: str, s: Solution) -> None:

        cls.trackers[tracker_group][tracker_name].append(s)

    @classmethod
    def update_tracker_group(cls, tracker_group: str, s: Solution) -> None:

        for tracker in cls.trackers[tracker_group].values():

            tracker.append(s)

    def _parse_target_tracker(self, tracker_target: str) -> dict[str, str]:

        group, tracker = tracker_target.split("/")
        return {"group": group, "tracker": tracker}

    @staticmethod
    def __check_all_objects_are_trackers(trackers: Iterable[Tracker]) -> None:

        for tracker in trackers:

            TrackerUser.__check_is_tracker(tracker)

    @staticmethod
    def __check_is_tracker(tracker_object: Tracker) -> None:

        if not isinstance(tracker_object, Tracker):

            raise TypeError("Dictionary values must be of Tracker type")
