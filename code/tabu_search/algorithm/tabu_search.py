from typing import Iterable
from ..decisions.reinitialization.base import ReinitializationCriterion
from ..decisions.stopping.base import StoppingCriterion
from ..initialization.base import SearchInitializer
from ..monitoring.base import Monitor
from ..neighbor_selection.base import NeighborSelector
from ..neighborhood_generation.base import NeighborhoodGenerator
from ..reinitialization.base import SearchReinitializer
from ..result_processing.base import Plot, PostProcessor, Syncer, Writer

class TabuSearch:

    def __init__(self, random_generator, monitors: Iterable[Monitor], post_processors: Iterable[PostProcessor],
                        plots: Iterable[Plot], result_writers: Iterable[Writer], result_syncers: Iterable[Syncer],
                        stopping_criterion: StoppingCriterion, reinitialization_criterion: ReinitializationCriterion,
                        initializer: SearchInitializer, reinitializer: SearchReinitializer, neighborhood_generator: NeighborhoodGenerator,
                        neighbor_selector: NeighborSelector) -> None:

        self.random_generator = random_generator
        self.monitors = monitors
        self.post_processors = post_processors
        self.plots = plots
        self.result_writers = result_writers
        self.result_syncers = result_syncers
        self.stopping_criterion = stopping_criterion
        self.reinitialization_criterion = reinitialization_criterion
        self.initializer = initializer
        self.reinitializer = reinitializer
        self.neighborhood_generator = neighborhood_generator
        self.neighbor_selector = neighbor_selector

    def tabu_search(self) -> None:

        self.__start_monitoring()
        self.initializer.initialize_search(self.random_generator)

        while not self.stopping_criterion.should_stop():

            neighborhood = self.neighborhood_generator.generate_neighborhood(self.random_generator)
            self.neighbor_selector.select_next_solution(neighborhood)

            if self.reinitialization_criterion.should_reinitialize():

                self.reinitializer.reinitialize_search(self.random_generator)

        self.__stop_monitoring()
        self.__post_process_results()
        self.__store_results()
        self.__plot_results()
        self.__sync_results()

    def __start_monitoring(self) -> None:

        for monitor_object in self.monitors:

            monitor_object.start()

    def __stop_monitoring(self) -> None:

        for monitor_object in self.monitors:

            monitor_object.stop()

    def __post_process_results(self) -> None:

        for post_processor_object in self.post_processors:

            post_processor_object.post_process()

    def __store_results(self) -> None:

        for writer_object in self.result_writers:

            writer_object.write()

    def __plot_results(self) -> None:

        for plot_object in self.plots:

            plot_object.plot()

    def __sync_results(self) -> None:

        for syncer_object in self.result_syncers:

            syncer_object.sync()
