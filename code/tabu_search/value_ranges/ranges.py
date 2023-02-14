from copy import deepcopy
from numbers import Number, Integral
from .base import ValueRange

"""Generic range interface for continuous numerical ranges"""
class NumericalRange(ValueRange):

    """Stores a tuple that represents the minimum and maximum
        values allowed for the attribute"""
    def __init__(self, range: list[Number] | tuple[Number]):

        self.set_range(range)

    def set_range(self, range: list[Number] | tuple[Number]) -> None:

        NumericalRange.__check_format(range)
        NumericalRange.__check_numerical(range)
        NumericalRange.__check_correct_range(range)

        self.__range_tuple = tuple(range)

    @staticmethod
    def __check_format(range: list[Number] | tuple[Number]) -> None:

        if not isinstance(range, tuple) and not isinstance(range, list):

            raise TypeError("Numerical range must be specified as a tuple or list")

    @staticmethod
    def __check_numerical(range: list[Number] | tuple[Number]) -> None:

        if not all([isinstance(value, Number) for value in range]):

            raise TypeError("Range must be numerical")

    @staticmethod
    def __check_correct_range(range: list[Number] | tuple[Number]) -> None:

        if not range[0] < range[1]:

            raise ValueError("First value must be smaller than second value")

    """Checks whether a value is contained within the stored range"""
    def __contains__(self, value: Number) -> bool:

        return self.__range_tuple[0] <= value <= self.__range_tuple[1]

    """Returns the minimum value of the range"""
    def min(self) -> Number:

        return self.__range_tuple[0]

    """Returns the maximum value of the range"""
    def max(self) -> Number:

        return self.__range_tuple[1]

    """Returns a random value contained within the stored range"""
    def random_value(self, generator) -> Number:

        if isinstance(self.__range_tuple[0], Integral):

            return generator.integers(self.__range_tuple[0], self.__range_tuple[1], endpoint = True)

        else:

            range_size = self.__range_tuple[1] - self.__range_tuple[0]
            return generator.random() * range_size + self.__range_tuple[0]

class CategoricalRange(ValueRange):

    """Stores a list of the possible values an attribute can take"""
    def __init__(self, range: list[Number] | tuple[Number]):

        self.set_range(range)

    def set_range(self, range: list[Number] | tuple[Number]) -> None:

        CategoricalRange.__check_format(range)

        self.__range_list = list(range)

    @staticmethod
    def __check_format(range: list[Number] | tuple[Number]) -> None:

        if not isinstance(range, tuple) and not isinstance(range, list):

            raise TypeError("Categorical range must be specified as a tuple or list of values")

    """Checks whether a value is contained within the stored range"""
    def __contains__(self, value) -> bool:

        return value in self.__range_list

    """Returns a random value contained within the stored range"""
    def random_value(self, generator):

        return self.__range_list[generator.integers(len(self.__range_list))]

    """Returns random values excluding the one passed as argument"""
    def random_values_without(self, excluded_value, how_many: int, generator):

        new_range = deepcopy(self.__range_list)
        new_range.remove(excluded_value)

        if how_many > len(new_range):

            raise ValueError("More values requested than available")

        return generator.choice(new_range, size = how_many, replace = False)
