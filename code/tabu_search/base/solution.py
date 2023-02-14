from math import inf
from numbers import Number
from typing import Any

"""Solution base class"""
class Solution:

    """Contains a particular parameter or value choice. Can also store
        its fitness score once evaluated"""
    def __init__(self, attributes: dict[str, Any], fitness: Number = -inf, reinitialized: bool = False):

        """'attributes' is a dictionary of pairs {name: value}"""
        self.attributes = attributes
        self.fitness = fitness
        self.reinitialized = reinitialized

    def to_dict(self) -> dict:

        return {"attributes": self.attributes, "fitness": self.fitness, "reinitialized": self.reinitialized}

    """Two Solution instances are equivalent if all their elements are equal"""
    def __eq__(self, other: 'Solution') -> bool:

        return all([self.attributes[k] == other.attributes[k]
                    for k in self.attributes.keys()])

    def __lt__(self, other: 'Solution') -> bool:

        if not self.is_evaluated() or self.fitness < other.fitness:

            return True

        else:

            return False

    def __ge__(self, other: 'Solution') -> bool:

        return other.__le__(self)

    def __le__(self, other: 'Solution') -> bool:

        if not self.is_evaluated() or self.fitness <= other.fitness:

            return True

        else:

            return False

    def __gt__(self, other: 'Solution') -> bool:

        return other.__lt__(self)

    """Tells whether a solution has already been evaluated (initially, it has not)"""
    def is_evaluated(self) -> bool:

        return self.fitness != -inf

    def set_reinitialization_flag(self) -> None:

        self.reinitialized = True

    def get_reinitialization_flag(self) -> None:

        return self.reinitialized
