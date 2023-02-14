from ...base.solution import Solution
from ..base import PostProcessor
from ...base.evaluator_user import EvaluatorUser

class PostEvaluator(PostProcessor, EvaluatorUser):

    def __init__(self, evaluator: str, evaluation_tracker: str, model_tracker: str):

        self.evaluator = evaluator
        self.evaluation_tracker: dict[str, str] = self._parse_target_tracker(evaluation_tracker)
        self.model_tracker: dict[str, str] = self._parse_target_tracker(model_tracker)
        self.create_tracker(self.model_tracker["group"], self.model_tracker["tracker"], "model")
        self.create_tracker(self.evaluation_tracker["group"], self.evaluation_tracker["tracker"], "fitness_history")

    def post_process(self) -> None:

        output_solution: Solution = self.trackers["progress"]["best_solution_history"].get_last()

        if self.trackers[self.model_tracker["group"]][self.model_tracker["tracker"]].empty():

            model = self.evaluators["final"][self.evaluator].create_and_fit_model(output_solution)
            output_solution.fitness = self.evaluators["final"][self.evaluator].evaluate_model(model)
            self.__save_model(model)

        else:

            model = self.trackers[self.model_tracker["group"]][self.model_tracker["tracker"]].get_last()
            output_solution.fitness = self.evaluators["final"][self.evaluator].evaluate_model(model)

        self.__save_evaluation(output_solution)

    def __save_model(self, model) -> None:

        self.trackers[self.model_tracker["group"]][self.model_tracker["tracker"]].append(model)

    def __save_evaluation(self, solution: Solution) -> None:

        self.trackers[self.evaluation_tracker["group"]][self.evaluation_tracker["tracker"]].append(solution)
