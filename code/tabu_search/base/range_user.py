from .solution import Solution
from ..value_ranges.base import ValueRange

"""Base class to give components the ability to access attribute value ranges"""
class AttributeRangeUser:

    _attr_ranges: dict[ValueRange] = {}

    """Stores attribute ranges (ValueRange objects) that delimit the search space"""
    @classmethod
    def set_attribute_ranges(cls, ranges: dict[ValueRange]) -> None:

        cls.__check_all_ranges_are_valueranges(ranges.values())

        cls._attr_ranges = ranges

    @staticmethod
    def __check_all_ranges_are_valueranges(ranges: list[ValueRange]) -> None:

        for range in ranges:

            AttributeRangeUser.__check_is_valuerange(range)

    @staticmethod
    def __check_is_valuerange(range_object: ValueRange) -> None:

        if not isinstance(range_object, ValueRange):

            raise TypeError("Dictionary values must be of ValueRange type")

    @classmethod
    def set_attribute_range(cls, range: dict[str, ValueRange]) -> None:

        attribute, range_object = next(iter(range.items()))
        cls.__check_is_valuerange(range_object)

        cls._attr_ranges[attribute] = range_object

    @classmethod
    def delete_attribute(cls, attribute: str) -> None:

        if attribute not in cls._attr_ranges:

            raise ValueError("Attribute range not stored")

        else:

            cls._attr_ranges.pop(attribute, None)

    """Tells whether a Solution is allowed according to the search ranges"""
    @classmethod
    def is_solution_valid(cls, s: Solution) -> bool:

        if cls._attr_ranges:

            return all([value in cls._attr_ranges[attr] for attr, value in s.attributes.items()])

        else:

            raise ValueError("No attribute ranges stored")
