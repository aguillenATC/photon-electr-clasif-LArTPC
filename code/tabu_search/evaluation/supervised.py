from ..base.solution import Solution
from sklearn.model_selection import cross_val_score, KFold, StratifiedKFold
from sklearn.metrics import accuracy_score, roc_auc_score, recall_score, precision_score, cohen_kappa_score, confusion_matrix
from .base import SupervisedEvaluator

class CrossValidationEvaluator(SupervisedEvaluator):

    def __init__(self, paradigm: str, fixed_model_parameters: dict, folds: int, is_stratified: bool, split = "val", seed = 42):

        super().__init__(paradigm = paradigm, fixed_model_parameters = fixed_model_parameters, split = split, seed = seed)
        self.folds = folds
        self.fold_creator = StratifiedKFold if is_stratified else KFold
        self.id = "cv"

    def evaluate(self, s: Solution) -> Solution:

        model = self.create_model(s)
        s.fitness = self.evaluate_model(model)
        return s

    def evaluate_model(self, model) -> float:

        folds = self.fold_creator(n_splits = self.folds, shuffle = True, random_state = self.seed)
        return cross_val_score(estimator = model, X = self.dataset[self.split], y = self.labels[self.split],
                                cv = folds).mean()

class AccuracyEvaluator(SupervisedEvaluator):

    def __init__(self, paradigm: str, fixed_model_parameters: dict, split = "val", **_):

        super().__init__(paradigm = paradigm, fixed_model_parameters = fixed_model_parameters, split = split)
        self.id = "accuracy"

    def evaluate(self, s: Solution, return_model = False) -> Solution:

        trained_model = self.create_and_fit_model(s)
        s.fitness = self.evaluate_model(trained_model)

        return s if not return_model else (s, trained_model)

    def evaluate_model(self, model) -> float:

        return accuracy_score(y_true = self.labels[self.split], y_pred = model.predict(self.dataset[self.split]))

class AUCEvaluator(SupervisedEvaluator):

    def __init__(self, paradigm: str, fixed_model_parameters: dict, split = "val", **_):

        super().__init__(paradigm = paradigm, fixed_model_parameters = fixed_model_parameters, split = split)
        self.id = "auc"

    def evaluate(self, s: Solution, return_model = False) -> Solution:

        trained_model = self.create_and_fit_model(s)
        s.fitness = self.evaluate_model(trained_model)

        return s if not return_model else (s, trained_model)

    def evaluate_model(self, model) -> float:

        return roc_auc_score(y_true = self.labels[self.split], y_score = model.predict(self.dataset[self.split]))

class RecallEvaluator(SupervisedEvaluator):

    def __init__(self, paradigm: str, fixed_model_parameters: dict, split = "val", **_):

        super().__init__(paradigm = paradigm, fixed_model_parameters = fixed_model_parameters, split = split)
        self.id = "recall" # Also called sensitivity.

    def evaluate(self, s: Solution, return_model = False) -> Solution:

        trained_model = self.create_and_fit_model(s)
        s.fitness = self.evaluate_model(trained_model)

        return s if not return_model else (s, trained_model)

    def evaluate_model(self, model) -> float:

        return recall_score(y_true = self.labels[self.split], y_pred = model.predict(self.dataset[self.split]))

class SpecificityEvaluator(SupervisedEvaluator):

    def __init__(self, paradigm: str, fixed_model_parameters: dict, split = "val", **_):

        super().__init__(paradigm = paradigm, fixed_model_parameters = fixed_model_parameters, split = split)
        self.id = "specificity"

    def evaluate(self, s: Solution, return_model = False) -> Solution:

        trained_model = self.create_and_fit_model(s)
        s.fitness = self.evaluate_model(trained_model)

        return s if not return_model else (s, trained_model)

    def evaluate_model(self, model) -> float:

        conf_matrix = confusion_matrix(y_true = self.labels[self.split], y_pred = model.predict(self.dataset[self.split]))
        return conf_matrix[0, 0] / (conf_matrix[0, 0] + conf_matrix[0, 1]) # Specificity = TN/(TN+FP)

class PrecisionEvaluator(SupervisedEvaluator):

    def __init__(self, paradigm: str, fixed_model_parameters: dict, split = "val", **_):

        super().__init__(paradigm = paradigm, fixed_model_parameters = fixed_model_parameters, split = split)
        self.id = "precision" # Also called positive predictive value (PPV)

    def evaluate(self, s: Solution, return_model = False) -> Solution:

        trained_model = self.create_and_fit_model(s)
        s.fitness = self.evaluate_model(trained_model)

        return s if not return_model else (s, trained_model)

    def evaluate_model(self, model) -> float:

        return precision_score(y_true = self.labels[self.split], y_pred = model.predict(self.dataset[self.split]))

class NPVEvaluator(SupervisedEvaluator):

    def __init__(self, paradigm: str, fixed_model_parameters: dict, split = "val", **_):

        super().__init__(paradigm = paradigm, fixed_model_parameters = fixed_model_parameters, split = split)
        self.id = "npv"

    def evaluate(self, s: Solution, return_model = False) -> Solution:

        trained_model = self.create_and_fit_model(s)
        s.fitness = self.evaluate_model(trained_model)

        return s if not return_model else (s, trained_model)

    def evaluate_model(self, model) -> float:

        conf_matrix = confusion_matrix(y_true = self.labels[self.split], y_pred = model.predict(self.dataset[self.split]))
        return conf_matrix[0, 0] / (conf_matrix[0, 0] + conf_matrix[1, 0]) # NPV = TN/(TN+FN)

class KappaEvaluator(SupervisedEvaluator):

    def __init__(self, paradigm: str, fixed_model_parameters: dict, split = "val", **_):

        super().__init__(paradigm = paradigm, fixed_model_parameters = fixed_model_parameters, split = split)
        self.id = "kappa"

    def evaluate(self, s: Solution, return_model = False) -> Solution:

        trained_model = self.create_and_fit_model(s)
        s.fitness = self.evaluate_model(trained_model)

        return s if not return_model else (s, trained_model)

    def evaluate_model(self, model) -> float:

        return cohen_kappa_score(y1 = self.labels[self.split], y2 = model.predict(self.dataset[self.split]))

class PrecisionRecallProductEvaluator(SupervisedEvaluator):

    def __init__(self, paradigm: str, fixed_model_parameters: dict, split = "val", **_):

        super().__init__(paradigm = paradigm, fixed_model_parameters = fixed_model_parameters, split = split)
        self.id = "precision_recall_product"

    def evaluate(self, s: Solution, return_model = False) -> Solution:

        trained_model = self.create_and_fit_model(s)
        s.fitness = self.evaluate_model(trained_model)

        return s if not return_model else (s, trained_model)

    def evaluate_model(self, model) -> float:

        recall = recall_score(y_true = self.labels[self.split], y_pred = model.predict(self.dataset[self.split]))
        precision = precision_score(y_true = self.labels[self.split], y_pred = model.predict(self.dataset[self.split]))

        return recall * precision
