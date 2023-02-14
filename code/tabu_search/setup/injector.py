from numpy import load
from numpy.random import default_rng
from ..config_parsing.yaml_parser import Parser
from ..value_ranges.factory import RangeFactory
from ..tracking.factory import TrackerFactory
from ..monitoring.factory import MonitorFactory
from ..result_processing.post_processing.factory import PostProcessorFactory
from ..result_processing.gfx.factory import PlotFactory
from ..result_processing.storage.factory import WriterFactory
from ..result_processing.upload.factory import SyncerFactory
from ..evaluation.factory import EvaluatorFactory
from ..decisions.stopping.factory import StoppingCriterionFactory
from ..initialization.factory import InitializerFactory
from ..reinitialization.factory import ReinitializerFactory
from ..decisions.reinitialization.factory import ReinitializationCriterionFactory
from ..neighborhood_generation.factory import NeighborhoodGeneratorFactory
from ..neighbor_selection.factory import NeighborSelectorFactory
from ..base.tabu_list import TabuList
from ..base.range_user import AttributeRangeUser
from ..base.tracker_user import TrackerUser
from ..base.evaluator_user import EvaluatorUser
from ..result_processing.base import ResultProcessor, Plot, Writer
from ..algorithm.tabu_search import TabuSearch

class Injector:

    def __init__(self, config_filename):

        self.__parser = Parser(config_filename)

    def create_tabu_search(self):

        self.set_attribute_ranges()
        self.set_evaluators()
        self.set_trackers()

        tabu_search = TabuSearch(random_generator = self.create_random_generator(),
                                 plots = self.create_plots(),
                                 monitors = self.create_monitors(),
                                 post_processors = self.create_post_processors(),
                                 result_writers = self.create_result_writers(),
                                 result_syncers = self.create_result_syncers(),
                                 stopping_criterion = self.create_stopping_criterion(),
                                 reinitialization_criterion = self.create_reinitialization_criterion(),
                                 initializer = self.create_initializer(),
                                 reinitializer = self.create_reinitializer(),
                                 neighborhood_generator = self.create_neighborhood_generator(),
                                 neighbor_selector = self.create_neighbor_selector())

        self.__parser.save_config_with_results()
        return tabu_search

    def create_random_generator(self):

        return default_rng(self.__parser.get_random_seed())

    def set_trackers(self):

        tracker_config = self.__parser.get_trackers_config()

        for tracker_group_name, tracker_group in tracker_config.items():

            tracker_dict = {tracker_name: TrackerFactory.create_tracker(tracker_name, config)
                                for tracker_name, config in tracker_group.items()}
            TrackerUser.set_tracker_group(tracker_group_name, tracker_dict)

    def create_monitors(self):

        monitoring_config = self.__parser.get_monitoring_config()

        return [MonitorFactory.create_monitor(config["type"], config["parameters"])
                            for config in monitoring_config]

    def create_post_processors(self):

        processing_config = self.__parser.get_result_processing_config()

        if "post_processing" in processing_config:

            post_processing_config = processing_config["post_processing"]
            return [PostProcessorFactory.create_post_processor(config["type"], config["parameters"])
                    for config in post_processing_config]

        else:

            return {}

    def create_plots(self):

        processing_config = self.__parser.get_result_processing_config()

        if "plots" in processing_config:

            ResultProcessor.set_results_path(processing_config["path"])
            Plot.set_subfolder(processing_config["plots_subfolder"])
            plot_configs = processing_config["plots"]
            return [PlotFactory.create_plot(config["type"], config["parameters"]) for config in plot_configs]

        else:

            return {}

    def create_result_writers(self):

        processing_config = self.__parser.get_result_processing_config()
        ResultProcessor.set_results_path(processing_config["path"])
        Writer.set_subfolder(processing_config["files_subfolder"])
        writer_configs = processing_config["files"]
        return [WriterFactory.create_writer(config["type"], config["parameters"]) for config in writer_configs]

    def create_result_syncers(self):

        processing_config = self.__parser.get_result_processing_config()

        if "syncing" in processing_config:

            ResultProcessor.set_results_path(processing_config["path"])
            syncer_configs = processing_config["syncing"]
            return [SyncerFactory.create_syncer(config["type"], config["parameters"]) for config in syncer_configs]

        else:

            return {}

    def create_stopping_criterion(self):

        stop_config = self.__parser.get_stopping_criterion_config()
        return StoppingCriterionFactory.create_stopping_criterion(stop_config["type"], stop_config["parameters"])

    def create_initializer(self):

        init_config = self.__parser.get_initializer_config()
        initializer = InitializerFactory.create_initializer(init_config["type"], init_config["parameters"])
        return initializer

    def set_attribute_ranges(self):

        range_config = self.__parser.get_attribute_ranges()
        formatted_ranges = {attribute: RangeFactory.create_range(info["type"], {"range": info["range"]})
                            for attribute, info in range_config.items()}

        AttributeRangeUser.set_attribute_ranges(formatted_ranges)

    def create_reinitializer(self):

        reinit_config = self.__parser.get_reinitializer_config()
        return ReinitializerFactory.create_reinitializer(reinit_config["type"], reinit_config["parameters"])

    def create_reinitialization_criterion(self):

        reinit_crit_config = self.__parser.get_reinitialization_criterion_config()
        return ReinitializationCriterionFactory.create_reinitialization_criterion(reinit_crit_config["type"], reinit_crit_config["parameters"])

    def create_neighborhood_generator(self):

        neigh_gen_config = self.__parser.get_neighborhood_generator_config()
        return NeighborhoodGeneratorFactory.create_neighborhood_generator(neigh_gen_config["type"], neigh_gen_config["parameters"])

    def set_evaluators(self):

        eval_config = self.__parser.get_evaluation_config()
        evaluator_seed = self.__parser.get_random_seed()
        evaluators_config = eval_config["evaluators"]

        evaluators_dict = {"fitness": EvaluatorFactory.create_evaluator(evaluators_config["fitness"]["type"],
                                                                        evaluators_config["fitness"]["parameters"]),
                           "final": {config["type"]: EvaluatorFactory.create_evaluator(config["type"], config["parameters"])
                                                                      for config in evaluators_config["final"]}}

        dataset_split = {split: load(file_path) for split, file_path in self.__parser.get_dataset_load_paths().items()}
        labels_split = {split: load(file_path) for split, file_path in self.__parser.get_labels_load_paths().items()}

        evaluators_dict["fitness"].set_dataset(dataset_split, labels_split)
        evaluators_dict["fitness"].set_parallel_jobs(eval_config["n_jobs"])
        evaluators_dict["fitness"].set_seed(evaluator_seed)

        for final_evaluator in evaluators_dict["final"].values():

            final_evaluator.set_dataset(dataset_split, labels_split)
            final_evaluator.set_parallel_jobs(eval_config["n_jobs"])
            final_evaluator.set_seed(evaluator_seed)

        EvaluatorUser.set_evaluators(evaluators_dict)

    def create_neighbor_selector(self):

        neigh_sel_config = self.__parser.get_neighbor_selector_config()
        tabu_tenures = self.__parser.get_attribute_tabu_tenures()
        return NeighborSelectorFactory.create_neighbor_selector(neigh_sel_config["type"],
                                                                {**neigh_sel_config["parameters"], "tabu_list": TabuList(tabu_tenures)})
