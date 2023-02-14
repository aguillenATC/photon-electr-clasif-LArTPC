from ..base import Writer
from .writers import CSVWriter, ModelWriter

class WriterFactory:

    writer_mapping = {"csv": CSVWriter, "model": ModelWriter}

    @classmethod
    def create_writer(cls, type, parameters = {}) -> Writer:

        return cls.writer_mapping[type](**parameters)
