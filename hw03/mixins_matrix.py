import numbers
import numpy as np

from pathlib import Path


class FromNdarrayMixin:
    @classmethod
    def from_ndarray(cls, arr: np.ndarray):
        return cls(value=arr)


class NdarrayStrMixin:
    def __str__(self) -> str:
        return self.value.__str__()


class NdarrayReprMixin:
    def __repr__(self) -> str:
        return self.value.__repr__().replace('array', type(self).__name__, 1)


class DumpReprMixin:
    def dump(self, file: Path):
        with file.open('w') as out:
            out.write(self.__repr__())


class NdarrayPropertiesMixin:
    @property
    def data(self):
        return self.value

    @data.setter
    def data(self, new_value: np.ndarray):
        self.value = new_value

    @property
    def shape(self):
        return self.value.shape


class MixinsMatrix(np.lib.mixins.NDArrayOperatorsMixin,
                   NdarrayReprMixin,
                   NdarrayStrMixin,
                   DumpReprMixin,
                   NdarrayPropertiesMixin,
                   FromNdarrayMixin):
    def __init__(self, value: np.ndarray):
        self.value = np.asarray(value)

    _HANDLED_TYPES = (np.ndarray, numbers.Number)

    def __array_ufunc__(self, ufunc, method, *args, **kwargs):
        args_value_unwrapped = (
            arg.value
            if isinstance(arg, MixinsMatrix) else arg
            for arg in args
        )

        result = getattr(ufunc, method)(*args_value_unwrapped, **kwargs)

        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            return None

        return type(self)(result)
