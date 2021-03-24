from abc import ABC
from typing import List, Union
import numpy as np
from rule.activation import Activation


class Condition(ABC):

    def __init__(self, features_indexes: Union[List[int], None] = None,
                 features_names: Union[List[str], None] = None,
                 empty: bool = False):
        if empty:
            self._features_indexes = None
        else:
            if features_indexes is None:
                raise ValueError("Must specify features_indexes")
        self._features_indexes = features_indexes
        if features_names is not None:
            self._features_names = features_names
        else:
            self._features_names = ["X_" + str(i) for i in self._features_indexes]

    def __and__(self, other: "Condition"):
        args = [i+j for i, j in zip(self.getattr, other.getattr)]
        return Condition(features_indexes=args[0], empty=False)

    def __add__(self, other: "Condition"):
        return self & other

    @property
    def getattr(self):
        return [self.features_indexes]

    @property
    def features_names(self) -> List[str]:
        return self._features_names

    @property
    def features_indexes(self) -> List[int]:
        return self._features_indexes

    @features_names.setter
    def features_names(self, values: Union[List[str], str]):
        if isinstance(values, str):
            values = (
                values.replace("[", "").replace("]", "").replace(" ", "").replace("'", "").replace('"', "").split(",")
            )
        self._features_names = values

    @features_indexes.setter
    def features_indexes(self, value: Union[List[int], str]):
        if isinstance(value, str):
            value = [int(v) for v in value.replace("[", "").replace("]", "").replace(" ", "").split(",")]
        self._features_indexes = value

    def __len__(self):
        return len(self._features_indexes)

    def evaluate(self, xs: np.ndarray) -> Activation:
        """
        Evaluates where a condition if fullfilled

        Parameters
        ----------
        xs: np.ndarray
            shape (n, d), n number of line, d number of features

        Returns
        -------
        activation: np.ndarray
             Shape  (n, 1). The activation vector, filled with 0 where the condition is met and 1 where it is not.
        """
        activation = np.ones(xs.shape[0])
        return Activation(activation)

    def intersect_condition(self, other):
        """To be implemented in daughter class"""
        pass
