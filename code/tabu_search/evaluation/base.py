from abc import ABC, abstractmethod
from ..base.solution import Solution
from joblib import Parallel, delayed
from multiprocessing import cpu_count
from .models.factory import ModelFactory

"""Generic Solution evaluator (fitness function) interface"""
class Evaluator(ABC):

    n_jobs = 1
    seed = 42

    """Contains the necessary fixed parameters to evaluate a Solution
        (for example, a dataset)"""
    @abstractmethod
    def __init__(self):

        raise NotImplementedError

    @classmethod
    def set_parallel_jobs(cls, jobs) -> None:

        if jobs < -1 or jobs > cpu_count():

            raise ValueError("Number of jobs must be -1 (all cores) or within the range of physical cores")

        cls.n_jobs = jobs

    @classmethod
    def set_seed(cls, seed) -> None:

        cls.seed = seed

    def evaluate_batch(self, solution_batch) -> list[Solution]:

        with Parallel(n_jobs = self.n_jobs, backend = "multiprocessing") as parallel:

            return parallel(delayed(self.evaluate)(solution)
                            for solution in solution_batch)

    """Evaluates a given Solution"""
    @abstractmethod
    def evaluate(self, s) -> Solution:

        raise NotImplementedError

class SupervisedEvaluator(Evaluator):

    dataset = None
    labels = None

    def __init__(self, paradigm: str, fixed_model_parameters: dict, split = "val"):

        self.paradigm = paradigm
        self.fixed_model_parameters = fixed_model_parameters if fixed_model_parameters else {}
        self.split = split

    def create_and_fit_model(self, s: Solution):

        model = self.create_model(s)
        model.fit(self.dataset["train"], self.labels["train"])
        return model

    def create_model(self, s: Solution):

        model_parameters: dict = {**s.attributes, **self.fixed_model_parameters}
        model = ModelFactory.create_model(self.paradigm, model_parameters)
        return model

    @classmethod
    def set_dataset(cls, dataset, labels) -> None:

        cls.dataset = dataset
        cls.labels = labels

    @abstractmethod
    def evaluate_model(self, model):

        raise NotImplementedError

    @abstractmethod
    def evaluate(self, s) -> Solution:

        raise NotImplementedError
