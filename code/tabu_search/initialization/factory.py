from ..initialization.base import SearchInitializer
from .initializers import RandomInitializer

class InitializerFactory():

    initializer_mapping = {"random": RandomInitializer}

    @classmethod
    def create_initializer(cls, type, parameters = {}) -> SearchInitializer:

        return cls.initializer_mapping[type](**parameters)
