from ..base import Plot
from .plots import ProgressPlot, SolutionSpaceCoverage, AttributeValueDistribution

class PlotFactory:

    plot_mapping = {"progress": ProgressPlot,
                    "space_coverage": SolutionSpaceCoverage,
                    "value_distribution": AttributeValueDistribution}

    @classmethod
    def create_plot(cls, type, parameters = {}) -> Plot:

        return cls.plot_mapping[type](**parameters)
