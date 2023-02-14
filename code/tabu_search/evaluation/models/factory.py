from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier, BaggingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.svm import LinearSVC
from xgboost import XGBClassifier

class ModelFactory():

    paradigm_mapping = {"random_forest": RandomForestClassifier,
                        "adaboost": AdaBoostClassifier,
                        "gradient_boosting": GradientBoostingClassifier,
                        "bagging": BaggingClassifier,
                        "log_reg": LogisticRegression,
                        "linear_svm": LinearSVC,
                        "xgboost": XGBClassifier,
                        "mlp": MLPClassifier}

    @classmethod
    def create_model(cls, paradigm, hyperparameters):

        return cls.paradigm_mapping[paradigm](**hyperparameters)
