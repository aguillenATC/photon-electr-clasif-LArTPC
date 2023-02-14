from .base import SearchReinitializer
from .reinitializers import RandomReinitializer

class ReinitializerFactory():

    reinitializer_mapping = {"random": RandomReinitializer}

    @classmethod
    def create_reinitializer(cls, type, parameters = {}) -> SearchReinitializer:

        return cls.reinitializer_mapping[type](**parameters)
