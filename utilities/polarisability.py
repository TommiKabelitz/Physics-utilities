import numpy as np
import pandas as pd

from utilities import configIDs, structure, fitting

Structure = structure.Structure

def get_energy_shift_fit_from_file(
    BF1_file: str,
    tmin: int,
    tmax: int,
):
    names = [
        "ts",
        "tf",
        "fmass",
        "fjerr",
        "ferr",
        "fbias",
        "chi2",
        "chi2dof",
        "gness",
        "ndof",
    ]

    df1 = pd.read_csv(BF1_file, delim_whitespace=True, header=None)
    df1.columns = names
    df1 = df1.query("ts == @tmin and tf == @tmax")
    df2 = pd.read_csv(BF1_file.replace("BF1","BF2"), delim_whitespace=True, header=None)
    df2.columns = names
    df2 = df2.query("ts == @tmin and tf == @tmax")
    vals = [df1["fmass"].iloc[0], df2["fmass"].iloc[0]]
    err = [df1["fjerr"].iloc[0], df2["fjerr"].iloc[0]]
    return vals, err

def get_energy_shift_from_file(
    BF1_file: str,
    t: int,
):
    names = [
        "t",
        "mass",
        "jerr",
        "bias",
    ]

    df1 = pd.read_csv(BF1_file, delim_whitespace=True, header=None)
    df1.columns = names
    df1 = df1.query("t == @t")
    df2 = pd.read_csv(BF1_file.replace("BF1","BF2"), delim_whitespace=True, header=None)
    df2.columns = names
    df2 = df2.query("t == @t")
    vals = [df1["mass"].iloc[0], df2["mass"].iloc[0]]
    err = [df1["jerr"].iloc[0], df2["jerr"].iloc[0]]
    return vals, err


def calculate_polarisability(
    data: list,
    particle: str,
    structure: Structure,
    ensemble: configIDs.PACSEnsemble = None,
    kappa: int = None,
    mass: float = None,
    verbose: bool = False,
    yerr: list = None,
) -> tuple[float, float]:

    if kappa is ensemble is None:
        raise ValueError("Require kappa or ensemble")
    elif ensemble is None:
        ensemble = configIDs.PACS_ensembles[kappa]
    if type(structure) is not Structure:
        structure = Structure(structure)

    if str(structure) != "uds":
        raise ValueError(f"Unsupported structure {structure}")
    if mass is None:
        mass = mass_dict[ensemble.kappa][particle]

    if verbose:
        print("data:", data, sep="\n")
        print("mass:", mass, sep="\n")
        
    fit = fitting.SimplePolarisabilityFit(
        particle,
        structure,
        ensemble,
        mass,
        np.array(data),
    )
    fit.do_fit()
    if verbose:
        print("dE-L:", fit.y, sep="\n")
        error_fit = fitting.curve_fit(fitting.PolarisabilityFit._quadfit,fit.x, fit.y, sigma=yerr, p0=fit.initial_guess)
        print(error_fit)
        print("Landau:", fit.landau_term,sep="\n")
    value, error, *_ = fit.fit
    value = fitting.PolarisabilityFit.convert_fit(value[0], fit.ensemble.a)
    error = fitting.PolarisabilityFit.convert_fit(error[0][0], fit.ensemble.a)
    return value, error

mass_dict = {
    13781: {
        "proton_1":9.790339025732240e-01,
        "neutron_1":9.760339025732240e-01,
        "sigmap_1":1.196169483041112E+00,
        "sigmam_1":1.196169483041112E+00,
        "cascade0_1": 1.295964084850002E+00,
        "cascadem_1": 1.295964084850002E+00,
        }
    }
