from .base import NeighborhoodGenerator
from .generators import FixedStepGenerator

class NeighborhoodGeneratorFactory():

    neighborhood_generator_mapping = {"fixed_step": FixedStepGenerator}

    @classmethod
    def create_neighborhood_generator(cls, type, parameters = {}) -> NeighborhoodGenerator:

        return cls.neighborhood_generator_mapping[type](**parameters)
