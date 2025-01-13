import functools
import os
import traceback
import numpy as np

# TODO: Update to allow 2nd order jackknives and also to allow multi-dim arrays
# TODO: Shouldn't allow passing of average and error in constructor, allows for bugs if passed incorrectly
#       and the speedup through not recalculating is essentially zero compared to all of the other things
#       that need to happen as part of the constructor


class JackknifeEnsemble:
    def __init__(
        self,
        jackknives: np.ndarray,
        ensemble_average=None,
        jackknife_error=None,
        axis: int = 0,
    ):
        if ensemble_average is not None and jackknife_error is not None:
            print("WARNING: ensemble_average and jackknife_error are passed to constructor. PLEASE CHANGE FOR FUTURE, STACK TRACE FOR REFERENCE:")
            traceback.print_stack()
        self.jackknives = (
            jackknives if type(jackknives) is np.ndarray else np.array(jackknives)
        )
        try:
            self.ncon = self.jackknives.shape[axis]
        except IndexError:
            raise ValueError(
                f"Axis {axis} out of bounds for array of shape {self.jackknives.shape}"
            )
        self.axis = axis

        if ensemble_average is not None:
            self.ensemble_average = ensemble_average
        else:
            self.ensemble_average = self._calculate_ensemble_average(
                self.jackknives, self.axis
            )
        if jackknife_error is not None:
            self.jackknife_error = jackknife_error
        else:
            self.jackknife_error = self._calculate_jackknife_error(
                self.jackknives, self.ensemble_average, axis=axis
            )

    @classmethod
    def init_jackknives_from_data(cls, data: np.ndarray, axis: int = 0):
        jackknives = cls.get_jackknives(data, axis)
        return cls(jackknives, axis=axis)

    @staticmethod
    def _calculate_ensemble_average(jackknives: np.ndarray, axis: int = 0):
        return jackknives.mean(axis=axis)

    @staticmethod
    def _calculate_jackknife_error(
        jackknives: np.ndarray, ensemble_average=None, axis: int = 0
    ):
        ncon = jackknives.shape[axis]
        if ensemble_average is None:
            ensemble_average = JackknifeEnsemble._calculate_ensemble_average(
                jackknives, axis=axis
            )
        return np.sqrt(
            np.sum((jackknives - broadcast(ensemble_average, axis=axis)) ** 2,axis=axis)
            / ncon
            * (ncon - 1)
        )

    @staticmethod
    def _calculate_uncertainties(data: np.ndarray, axis: int = 0) -> np.ndarray:
        ncon = data.shape[axis]
        variances = np.zeros(ncon)
        ensemble_squared = data**2

        sum_of_squares_term = (
            broadcast((data**2).sum(axis=axis), axis=axis) - ensemble_squared
        )
        squared_sum_term = (
            broadcast(data.sum(axis=axis) ** 2, axis=axis)
            + ensemble_squared
            - 2 * data * broadcast(data.sum(axis=axis), axis=axis)
        ) / (ncon - 1)
        variances = (ncon - 2) / (ncon - 1) * (sum_of_squares_term - squared_sum_term)
        return np.sqrt(variances)

    @staticmethod
    def get_jackknives(data: np.ndarray, axis: int = 0):
        return (broadcast(data.sum(axis=axis), axis=axis) - data) / (
            data.shape[axis] - 1
        )

    @functools.cached_property
    def uncertainties(self):
        return self._calculate_uncertainties(self.jackknives, axis=self.axis)

    @property
    def square_sum(self):
        return self.jackknives.sum(axis=self.axis) ** 2

    @property
    def sum_of_squares(self):
        return (self.jackknives**2).sum(axis=self.axis)

    @property
    def sum(self):
        return self.jackknives.sum(axis=self.axis)

    def write_jackknives(self, filepath: os.PathLike, **kwargs):
        if len(self.jackknives.shape) > 1:
            raise NotImplementedError("Only one dimensional arrays are supported for file writing.")
        np.savetxt(filepath, self.jackknives, *kwargs)

    @classmethod
    def from_file(cls, filepath: os.PathLike, **kwargs):
        jackknives = np.loadtxt(filepath, **kwargs)
        if jackknives.ndim != 1:
            raise NotImplementedError("Only one dimensional arrays are supported for file reading.")
        return cls(jackknives)

    def __add__(self, other):
        if type(other) is not type(self):
            try:
                jackknives = self.jackknives + other
            except TypeError:
                raise TypeError("Unsupported type for addition.")
            except Exception as e:
                raise e
        else:
            jackknives = self.jackknives + other.jackknives
        return JackknifeEnsemble(jackknives)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return -1 * other + self

    def __rsub__(self, other):
        retur - self + other

    def __mul__(self, other):
        if type(other) is not type(self):
            try:
                jackknives = self.jackknives * other
            except TypeError:
                raise TypeError("Unsupported type for multiplication.")
            except Exception as e:
                raise e
        else:
            jackknives = self.jackknives * other.jackknives
        return JackknifeEnsemble(jackknives)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, denom):
        return self * (1 / denom)

    def __rtruediv__(self, numer):
        if type(numer) is not type(self):
            try:
                jackknives = numer / self.jackknives
            except TypeError:
                raise TypeError("Unsupported type for division.")
            except Exception as e:
                raise e
        else:
            jackknives = numer.jackknives / self.jackknives
        return JackknifeEnsemble(jackknives)

    def __floordiv__(self, denom):
        if type(denom) is not type(self):
            try:
                jackknives = self.jackknives // denom
            except TypeError:
                raise TypeError("Unsupported type for floor division.")
            except Exception as e:
                raise e
        else:
            jackknives = self.jackknives // denom.jackknives
        return JackknifeEnsemble(jackknives)

    def __rfloordiv__(self, numer):
        if type(numer) is not type(self):
            try:
                jackknives = numer // self.jackknives
            except TypeError:
                raise TypeError("Unsupported type for floor division.")
            except Exception as e:
                raise e
        else:
            jackknives = numer.jackknives // self.jackknives
        return JackknifeEnsemble(jackknives)

    def __pow__(self, pow):
        if type(pow) is not type(self):
            try:
                jackknives = self.jackknives**pow
            except TypeError:
                raise TypeError("Unsupported type for exponentiation.")
            except Exception as e:
                raise e
        else:
            jackknives = self.jackknives**pow.jackknives
        return JackknifeEnsemble(jackknives)

    def __rpow__(self, base):
        if type(base) is not type(self):
            try:
                jackknives = base**self.jackknives
            except TypeError:
                raise TypeError("Unsupported type for exponentiation.")
            except Exception as e:
                raise e
        else:
            jackknives = base.jackknives**self.jackknives
        return JackknifeEnsemble(jackknives)


def broadcast(array: np.ndarray, axis: int):
    try:
        if len(array.shape) > axis+1:
            raise ValueError(
                f"Cannot broadcast to axis {axis} of array with shape {array.shape}"
            )
    except AttributeError:
        return array
    new_shape = list(array.shape)
    new_shape.insert(axis, 1)
    return array.reshape(new_shape)
