from ..value_ranges.base import ValueRange
from .ranges import NumericalRange, CategoricalRange

class RangeFactory():

    range_mapping = {"numerical": NumericalRange,
                            "categorical": CategoricalRange}

    @classmethod
    def create_range(cls, type, parameters) -> ValueRange:

        return cls.range_mapping[type](**parameters)
