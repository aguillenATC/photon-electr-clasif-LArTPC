from ..evaluation.base import Evaluator

"""Base class to give components the ability to the Solution fitness evaluators"""
class EvaluatorUser:

    evaluators: dict = {}

    @classmethod
    def set_evaluator(cls, evaluator_name: str, evaluator_object: Evaluator) -> None:

        cls.evaluators[evaluator_name] = evaluator_object

    @classmethod
    def set_evaluators(cls, evaluator_container: dict) -> None:

        cls.evaluators = evaluator_container
