from .base import Evaluator
from .supervised import CrossValidationEvaluator, AccuracyEvaluator, PrecisionEvaluator, RecallEvaluator, KappaEvaluator, AUCEvaluator, SpecificityEvaluator, NPVEvaluator, PrecisionRecallProductEvaluator

class EvaluatorFactory():

    evaluator_mapping = {"cv": CrossValidationEvaluator,
                         "accuracy": AccuracyEvaluator,
                         "precision": PrecisionEvaluator,
                         "recall": RecallEvaluator,
                         "precision_recall_product": PrecisionRecallProductEvaluator,
                         "kappa": KappaEvaluator,
                         "auc": AUCEvaluator,
                         "specificity": SpecificityEvaluator,
                         "npv": NPVEvaluator}

    @classmethod
    def create_evaluator(cls, type, parameters) -> Evaluator:

        return cls.evaluator_mapping[type](**parameters)
