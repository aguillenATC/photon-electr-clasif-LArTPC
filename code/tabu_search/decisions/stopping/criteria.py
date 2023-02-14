from .base import StoppingCriterion
from ...base.tracker_user import TrackerUser

class IterationLimit(StoppingCriterion, TrackerUser):

    def __init__(self, iteration_limit: int):

        IterationLimit.__check_valid_iteration_limit(iteration_limit)

        self.iteration_limit = iteration_limit

    @staticmethod
    def __check_valid_iteration_limit(iteration_limit: int) -> None:

        if iteration_limit <= 0:

            raise ValueError("Iteration limit must be a positive integer")

    def should_stop(self) -> bool:

        return self.trackers["progress"]["solution_history"].get_step_count() >= self.iteration_limit
