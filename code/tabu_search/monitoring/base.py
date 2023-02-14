from abc import ABC, abstractmethod
from ..base.tracker_user import TrackerUser

class Monitor(TrackerUser, ABC):

    @abstractmethod
    def start(self) -> None:

        raise NotImplementedError

    @abstractmethod
    def stop(self) -> None:

        raise NotImplementedError
