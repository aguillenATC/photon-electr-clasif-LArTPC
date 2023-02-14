from .base import Tracker
from .trackers import FitnessHistoryTracker, SolutionHistoryTracker, BestFitnessTracker, BestSolutionTracker, ModelTracker, TimeTracker, InstantaneousPowerTracker, AccumulatedEnergyTracker

class TrackerFactory:

    tracker_mapping = {"best_solution_history": BestSolutionTracker,
                        "solution_history": SolutionHistoryTracker,
                        "best_fitness_history": BestFitnessTracker,
                        "fitness_history": FitnessHistoryTracker,
                        "model": ModelTracker,
                        "time": TimeTracker,
                        "power": InstantaneousPowerTracker,
                        "energy": AccumulatedEnergyTracker}

    @classmethod
    def create_tracker(cls, type, parameters = {}) -> Tracker:

        return cls.tracker_mapping[type](**parameters)
