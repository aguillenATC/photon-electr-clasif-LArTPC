from .base import StoppingCriterion
from .criteria import IterationLimit

class StoppingCriterionFactory():

    stopping_criterion_mapping = {"iteration_limit": IterationLimit}

    @classmethod
    def create_stopping_criterion(cls, type, parameters = {}) -> StoppingCriterion:

        return cls.stopping_criterion_mapping[type](**parameters)
