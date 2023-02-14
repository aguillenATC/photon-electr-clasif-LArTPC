from .base import ReinitializationCriterion
from .criteria import NoReinitialization, ReinitializeIfStagnant

class ReinitializationCriterionFactory():

    reinitialization_criterion_mapping = {"no_reinitialization": NoReinitialization,
                                            "if_stagnant": ReinitializeIfStagnant}

    @classmethod
    def create_reinitialization_criterion(cls, type, parameters = {}) -> ReinitializationCriterion:

        return cls.reinitialization_criterion_mapping[type](**parameters)
