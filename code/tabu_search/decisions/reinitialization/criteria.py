from numbers import Number
from .base import ReinitializationCriterion
from ...base.tracker_user import TrackerUser

class NoReinitialization(ReinitializationCriterion):

    def should_reinitialize(self):

        return False

class ReinitializeIfStagnant(ReinitializationCriterion, TrackerUser):

    def __init__(self, progress_threshold: Number, steps_back: int):

        self.progress_threshold = progress_threshold
        self.steps_back = steps_back
        self.current_streak = 1

    def should_reinitialize(self) -> bool:

        if self.current_streak >= self.steps_back and \
                self.trackers["progress"]["fitness_history"].variation_last_n(self.steps_back) < self.progress_threshold:

            self.current_streak = 1
            return True

        else:

            self.current_streak += 1
            return False
