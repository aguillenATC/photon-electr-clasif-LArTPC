import os
import time
from random import getrandbits
from yaml import safe_load, dump

class Parser:

    def __init__(self, config_filename):

        self.__config = safe_load(open(config_filename))
        self.__set_tabu_search_seed()
        self.__add_run_date_to_results_path()

    def __set_tabu_search_seed(self):

        if "RANDOM_SEED" in os.environ and os.environ.get("RANDOM_SEED"):

            self.__config["random_seed"] = int(os.environ.get("RANDOM_SEED"))

        elif not ("random_seed" in self.__config and self.__config["random_seed"]):

            self.__config["random_seed"] = getrandbits(22)

    def __add_run_date_to_results_path(self):

        config = self.__config["results"]

        if config["append_time_to_path"]:

            config["path"] += time.strftime("%Y-%m-%d_%H:%M_", time.localtime()) + str(self.__config["random_seed"]) + "/"

    def save_config_with_results(self):

        config = self.__config["results"]

        if config["config_subfolder"]:

            save_path = config["path"] + config["config_subfolder"]

            if not os.path.isdir(save_path):

                os.makedirs(save_path)

            dump(self.__config, open(save_path + "config.yaml", "w"))

    def get_dataset_load_paths(self):

        folder_path = self.__config["evaluation"]["data_path"]

        return {dataset_split: folder_path + file_path
                for dataset_split, file_path in self.__config["evaluation"]["dataset_names"].items()}

    def get_labels_load_paths(self):

        folder_path = self.__config["evaluation"]["data_path"]

        return {labels_split: folder_path + file_path
                for labels_split, file_path in self.__config["evaluation"]["labels_names"].items()}

    def get_random_seed(self):

        return self.__config["random_seed"]

    def get_stopping_criterion_config(self):

        return self.__config["stopping_criterion"]

    def get_initializer_config(self):

        return self.__config["initialization"]

    def get_reinitializer_config(self):

        return self.__config["reinitialization"]

    def get_reinitialization_criterion_config(self):

        return self.__config["reinitialization_criterion"]

    def get_neighborhood_generator_config(self):

        return self.__config["neighborhood_generation"]

    def get_neighbor_selector_config(self):

        return self.__config["neighbor_selection"]

    def get_evaluation_config(self):

        return self.__config["evaluation"]

    def get_trackers_config(self):

        return self.__config["trackers"]

    def get_monitoring_config(self):

        return self.__config["monitoring"]

    def get_result_processing_config(self):

        return self.__config["results"]

    def get_attribute_ranges(self):

        return {attribute: {"range": info["range"], "type": info["type"]}
                    for attribute, info in self.__config["solution_ranges"].items()}

    def get_attribute_tabu_tenures(self):

        return self.__config["tabu_tenures"]
