from ..base import PostProcessor
from .post_processors import PostEvaluator

class PostProcessorFactory:

    post_processor_mapping = {"post_evaluator": PostEvaluator}

    @classmethod
    def create_post_processor(cls, type, parameters = {}) -> PostProcessor:

        return cls.post_processor_mapping[type](**parameters)
