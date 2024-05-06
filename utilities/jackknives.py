import functools
import os

import numpy as np

# TODO: Update to allow 2nd order jackknives and also to allow multi-dim arrays

class JackknifeEnsemble:
    def __init__(
        self, jackknives: np.ndarray, ensemble_average=None, jackknife_error=None
    ):
        self.jackknives = jackknives
        self.ncon = self.jackknives.size
        if ensemble_average is not None:
            self.ensemble_average = ensemble_average
        else:
            self.ensemble_average = self._calculate_ensemble_average(jackknives)
        if jackknife_error is not None:
            self.jackknife_error = jackknife_error
        else:
            self.jackknife_error = self._calculate_jackknife_error(
                jackknives, self.ensemble_average
            )


    @staticmethod
    def _calculate_ensemble_average(jackknives: np.ndarray):
        return jackknives.mean()

    @staticmethod
    def _calculate_jackknife_error(jackknives: np.ndarray, ensemble_average=None):
        if ensemble_average is None:
            ensemble_average = JackknifeEnsemble._calculate_ensemble_average(jackknives)
        return np.sqrt(
            np.sum((jackknives - ensemble_average) ** 2)
            * jackknives.size
            / (jackknives.size - 1)
        )

    # TODO make this static
    def _calculate_uncertainties(self) -> np.ndarray:
        ncon = self.ncon
        variances = np.zeros(ncon)
        ensemble_squared = self.jackknives**2

        sum_of_squares_term = self.sum_of_squares - ensemble_squared
        squared_sum_term = (
            self.square_sum + ensemble_squared - 2 * self.jackknives * self.sum
        ) / (ncon - 1)
        variances = (ncon - 2) / (ncon - 1) * (sum_of_squares_term - squared_sum_term)
        return np.sqrt(variances)

    @functools.cached_property
    def uncertainties(self):
        return self._calculate_uncertainties()

    @property
    def square_sum(self):
        return self.jackknives.sum() ** 2

    @property
    def sum_of_squares(self):
        return (self.jackknives**2).sum()

    @property
    def sum(self):
        return self.jackknives.sum()
    
    def write_jackknives(self, filepath: os.PathLike, **kwargs):
        np.savetxt(filepath, self.jackknives, *kwargs)
        
    @classmethod
    def from_file(cls, filepath: os.PathLike, **kwargs):
        jackknives = np.loadtxt(filepath, **kwargs)
        if jackknives.ndim != 1:
            raise ValueError("Contents of file must be one dimensional array.")
        return cls(jackknives)
    
    def __add__(self, other):
        jackknives = self.jackknives + other.jackknives
        return JackknifeEnsemble(jackknives)

    def __sub__(self, other):
        jackknives = self.jackknives - other.jackknives
        return JackknifeEnsemble(jackknives)

    def __mul__(self, other):
        jackknives = self.jackknives * other.jackknives
        return JackknifeEnsemble(jackknives)

    def __truediv__(self, other):
        jackknives = self.jackknives / other.jackknives
        return JackknifeEnsemble(jackknives)

    def __rtruediv__(self, other):
        jackknives = self.jackknives / other.jackknives
        return JackknifeEnsemble(jackknives)

    def __floordiv__(self, other):
        jackknives = self.jackknives // other.jackknives
        return JackknifeEnsemble(jackknives)

    def __pow__(self, pow):
        jackknives = self.jackknives ** pow
        return JackknifeEnsemble(jackknives)

