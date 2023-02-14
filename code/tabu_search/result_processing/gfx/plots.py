import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from ..base import Plot

class ProgressPlot(Plot):

    def __init__(self, plot: dict, save: dict, target_tracker: str):

        super().__init__(plot = plot, save = save, target_tracker = target_tracker)

    def plot(self) -> None:

        data: pd.Dataframe = self.get_target_tracker().to_dataframe()
        line_plot = sns.lineplot(data = data, **self.plot_params["general"])
        line_plot.set(**self.plot_params["axes"])
        line_plot.xaxis.set_major_locator(MaxNLocator(integer = True)) # Force integers in x-axis

        if self.save_params:

            self.__save_plot()

        else:

            plt.show()

        plt.clf()

    def __save_plot(self) -> None:

        save_path: str = self.results_path + self.subfolder

        self.check_and_create_folder_path(save_path)

        self.save_params["fname"] = save_path + self.save_params["fname"]
        plt.savefig(**self.save_params)

class SolutionSpaceCoverage(Plot):

    def __init__(self, plot: dict, save: dict, target_tracker: str):

        super().__init__(plot = plot, save = save, target_tracker = target_tracker)

    def plot(self) -> None:

        data: pd.DataFrame = self.get_target_tracker().to_dataframe()
        scatter_plot = sns.scatterplot(data = data, **self.plot_params["general"],
                                        size = "fitness", hue = "fitness", legend = "brief")
        scatter_plot.set(**self.plot_params["axes"])
        sns.move_legend(scatter_plot, "lower center", bbox_to_anchor = (.5, 1),
                        title = None, ncol = 5, frameon = False)

        if self.save_params:

            self.__save_plot()

        else:

            plt.show()

        plt.clf()

    def __save_plot(self) -> None:

        save_path: str = self.results_path + self.subfolder

        self.check_and_create_folder_path(save_path)

        self.save_params["fname"] = save_path + self.save_params["fname"]
        plt.savefig(**self.save_params)

class AttributeValueDistribution(Plot):

    def __init__(self, plot: dict, save: dict, target_tracker: str):

        super().__init__(plot = plot, save = save, target_tracker = target_tracker)

    def plot(self) -> None:

        data: pd.DataFrame = self.get_target_tracker().to_dataframe()
        density_plot = sns.kdeplot(data = data, **self.plot_params["general"])
        density_plot.set(**self.plot_params["axes"])

        if self.save_params:

            self.__save_plot()

        else:

            plt.show()

        plt.clf()

    def __save_plot(self) -> None:

        save_path: str = self.results_path + self.subfolder

        self.check_and_create_folder_path(save_path)

        self.save_params["fname"] = save_path + self.save_params["fname"]
        plt.savefig(**self.save_params)
