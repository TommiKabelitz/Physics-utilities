from __future__ import annotations 
import functools
import logging

import gvar as gv
import lsqfit as lsq
import natpy as nat
import numpy as np

from utilities import jackknives, structure, particles, configIDs



JackknifeEnsemble = jackknives.JackknifeEnsemble
Structure = structure.Structure


logger = logging.getLogger(__name__)
logging.Formatter(fmt="%(name)s(%(lineno)d)::%(levelname)-8s: %(message)s")


class Fit_1d:
    def __init__(
        self,
        fcn: callable,
        nparams: int,
        x: np.ndarray,
        y,
        y_err: np.ndarray = None,
        jackknives: list[JackknifeEnsemble] = None,
        initial_guess: list[float] = None,
        prior: dict[str,gv.gvar] = None,
        calculate_naive_chi_sq: bool = False,
        fit_jackknives: bool = False,
    ):
        self.fcn = fcn
        self.nparams = nparams
        self.x = x
        if isinstance(y[0], gv.GVar):
            if y_err is not None:
                logging.warning(
                    "y is array of gvar variables so passed y_err will be ignored."
                )
            if jackknives is not None and not fit_jackknives:
                logger.warning(
                    "Jackknives were supplied. Passing y as collection of gvar variables with fit_jackknives = False will result in the jackknives being ignored and the existing covariance between the gvars to be used instead."
                )
            elif jackknives is not None:
                logger.warning(
                    "Using existing correlation between the y data from gvars. Jackknives will only be used for the fit on a jackknife level."
                )

            # In case gvar were passed as a list
            self.y = gv.gvar(y)

        elif isinstance(y[0], (float, np.floating)):
            if y_err is jackknives is None:
                raise ValueError(
                    "y is array of floats so either y_err or jackknives must be non-None."
                )
            if y_err is None:
                logger.info(
                    "Setting uncertainties using covariance matrix from jackknives."
                )
                self.covariance_matrix = covariance_matrix(jackknives)
                self.y = gv.gvar(y, self.covariance_matrix)
            elif jackknives is None:
                self.y = gv.gvar(y, y_err)
        else:
            raise ValueError("y must be array of gvars or floats.")

        if initial_guess is None and prior is None:
            logger.info("Taking initial guess to be zero for all fit parameters.")
            self.initial_guess = [0] * self.nparams
        elif initial_guess is not None and prior is not None:
            raise ValueError("Cannot have non-None prior and initial guess.")
        else:
            self.initial_guess = initial_guess
            self.prior = prior

        self.calculate_naive_chi_sq = calculate_naive_chi_sq
        if fit_jackknives and jackknives is None:
            raise ValueError("Jackknives must not be None to be fit")
        self.jackknives = jackknives
        self.fit_jackknives = fit_jackknives

    def do_fit(self):
        self.average_fit = lsq.nonlinear_fit(
            data=(self.x, self.y), fcn=self.fcn, p0=self.initial_guess, prior=self.prior,
        )

        if self.calculate_naive_chi_sq or self.fit_jackknives:
            if self.prior is not None:
                guess_args = {"prior": self.prior}
            else:
                guess_args = {"p0": [gv.mean(self.average_fit.p)]}

        if self.calculate_naive_chi_sq:
            diagonal_covariance_mat = gv.evalcov(self.y) * np.eye(self.y.size)
            self.uncorrelated_y = gv.gvar(gv.mean(self.y), diagonal_covariance_mat)
            self.naive_fit = lsq.nonlinear_fit(
                data=(self.x, self.y), fcn=self.fcn, **guess_args
            )

        if self.fit_jackknives:
            self.jackknife_fits = []
            ncon = self.jackknives[0].ncon
            self.jackknife_fits_values = np.zeros(ncon)
            for icon in range(ncon):
                y_data = [
                    jackknife_ensemble.jackknives[icon]
                    for jackknife_ensemble in self.jackknives
                ]
                y_err = [
                    jackknife_ensemble.uncertainties[icon]
                    for jackknife_ensemble in self.jackknives
                ]
                
                self.jackknife_fits.append(
                    lsq.nonlinear_fit(
                        data=(self.x, y_data, y_err),
                        fcn=self.fcn,
                        **guess_args,
                    )
                )
                self.jackknife_fits_values[icon] = self.jackknife_fits[icon].pmean
            self.jackknife_fits_values = JackknifeEnsemble(self.jackknife_fits_values)

def covariance_matrix(jackknife_ensembles: list[JackknifeEnsemble]) -> np.ndarray:
    ensemble_averages = np.asarray(
        [ensemble.ensemble_average for ensemble in jackknife_ensembles]
    )
    product_of_average = ensemble_averages[:, None] * ensemble_averages[:, None].T
    jackknives = np.asarray([ensemble.jackknives for ensemble in jackknife_ensembles])
    ncon = jackknives.shape[1]
    average_of_product = np.matmul(jackknives, jackknives.T) / ncon
    return (ncon - 1) * (average_of_product - product_of_average)


class PolarisabilityFit(Fit_1d):
    def __init__(
        self,
        particle: str,
        structure: Structure,
        ensemble: configIDs.PACSEnsemble,
        mass: gv.GVar,
        energy_shift: np.ndarray,
        mass_jackknives: JackknifeEnsemble = None,
        energy_shift_jackknives: list[JackknifeEnsemble] = None,
        initial_guess: float = 0,
        calculate_naive_chi_sq: bool = True,
        fit_jackknives: bool = False,
    ):
        self.particle = particle
        self.structure = structure
        self.ensemble = ensemble
        self.mass = mass
        self.energy_shift = energy_shift
        self.num_kd = energy_shift.size

        x = np.arange(1, self.num_kd + 1)

        self.landau_term = self.calculate_landau(
            mass, particle, structure, spacing=ensemble.a
        )
        y = energy_shift - self.landau_term * x
        
        if fit_jackknives and None not in (mass_jackknives, energy_shift_jackknives):
            self.mass_jackknives = mass_jackknives
            self.energy_shift_jackknives = energy_shift_jackknives
            self.landau_jackknives = self.calculate_landau(
                self.mass_jackknives.jackknives, particle, structure, spacing=ensemble.a
            )
            jackknives = [JackknifeEnsemble(self.energy_shift_jackknives[i].jackknives - self.landau_jackknives * x[i]) for i in range(self.num_kd)]
            
        else:
            jackknives = None

        super().__init__(
            fcn=self._quadfit,
            nparams=1,
            x=x,
            y=y,
            jackknives=jackknives,
            initial_guess=[initial_guess],
            calculate_naive_chi_sq=calculate_naive_chi_sq,
            fit_jackknives=fit_jackknives,
        )

    @staticmethod
    def convert_fit(fit_value: gv.GVar | np.ndarray, spacing: float, Nx = 32, Ny = 32):
        HBARC = 0.1973269718  # GeV fm
        q_d = -1/3
        return (
            -2
            * fit_value
            * nat.constants.alpha.value
            * (-1 / 3) ** 2
            * (spacing**4 * (Nx * Ny / 2 / np.pi) ** 2 / HBARC)
        )

    @staticmethod
    def _quadfit(x, a0):
        return x**2 * a0

    @staticmethod
    def calculate_landau(
        mass: float | np.ndarray, particle: str, structure: Structure, spacing: float
    ) -> float | np.ndarray:
        
        particle_charge = particles.get_particle_charge(particle, structure)
        q_d = -1 / 3
        Nx = Ny = 32
        HBARC = 0.1973269718  # GeV fm
        landau = (
            abs(particle_charge / (q_d))
            * np.pi
            / Nx
            / Ny
            * (HBARC / spacing) ** 2
            / mass
        )
        return landau


if __name__ == "__main__":
    shift = np.asarray([0.0259, 0.0443])
    shift_err = np.asarray([0.0033, 0.0056])
    shift_gv = gv.gvar(shift, shift_err)
    mass = gv.gvar(1.053819, 0.011708)
    fit = PolarisabilityFit(
        "proton_1",
        Structure("uds"),
        configIDs.PACS_ensembles[13770]["a"],
        mass,
        shift_gv,
    )
    fit.do_fit()
    print(fit.average_fit)
    print(fit.convert_fit(fit.average_fit.pmean, fit.ensemble.a))