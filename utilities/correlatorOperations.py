import os
from pathlib import Path
import re

import numpy as np

from utilities import configIDs as cfg


kappa_pattern = re.compile(r"\/k(\d{5})\/")
kd_pattern = re.compile(r"\/BF([-+]?\d)\/")
shift_pattern = re.compile(r"\/sh(([xyzt]\d+)+|(None))\/")
source_pattern = re.compile(r"SO((sm|lp)\d+)")
sink_pattern = re.compile(r"si((sm|lp|ln)\d+)")
configID_pattern = re.compile(r"icfg(-(?:[ab]|[ghijk]M){1}-\d+)")
operator_pattern = re.compile(r"([\w\d_]+bar)_")
structure_pattern = re.compile(r"_([udsnlh]+).")


class CfunMomentum:
    def __init__(self, indices: list[int], label: str):
        self.indices = indices
        self.label = label
        self.dimension = len(self.indices)

    @property
    def str_indices(self):
        return " ".join([str(i) for i in self.indices])

    def __str__(self):
        return f"{self.label}: {self.str_indices}"


class ExceptionalConfig:
    def __init__(self, kappa: int, configID: cfg.ConfigID, shift: str):
        self.kappa = kappa
        self.configID = configID
        self.shift = shift

    def __hash__(self):
        return hash((self.kappa, self.configID, self.shift))

    def __eq__(self, other):
        return (self.kappa, str(self.configID), self.shift) == (
            other.kappa,
            str(other.configID),
            other.shift,
        )

    def __neq__(self, other):
        return not self == other

    @property
    def full_string(self):
        return f"{self.kappa} {str(self.configID)} {self.shift}"

    @staticmethod
    def init_from_string(exceptional_string: str):
        kappa, config_str, shift = exceptional_string.split(" ")
        configID = cfg.ConfigID(int(kappa), ID_str=config_str)
        return ExceptionalConfig(int(kappa), configID, shift)

    @staticmethod
    def init_from_cfun_path(cfun_path: os.PathLike):
        cfun = CfunMetadata(cfun_path)
        try:
            ExceptionalConfig(
                cfun.kappa, cfg.ConfigID(cfun.kappa, ID_str=cfun.configID), cfun.shift
            )
        except AttributeError:
            raise ValueError(
                "Could not extract kappa, configID and shift from cfun_path."
            )


class CfunMetadata:
    def __init__(self, cfun_path: os.PathLike):
        for prop, val in self.parse_cfun_path(cfun_path).items():
            if prop in ("kd", "kappa"):
                val = int(val)
            setattr(self, prop, val)
        self.cfun_path = cfun_path

    @staticmethod
    def parse_cfun_path(cfun_path: os.PathLike) -> dict:
        # /scratch/e31/tk9944/WorkingStorage/PhDRunThree/k13781/BF1/cfuns/shx23y08z26t00/SOsm250_icfg-kM-001630silp96.cascade0_1cascade0_1bar_uds.u.2cf
        # kappa, kd, shift, source, configID, sink, operator, operatorbar, structure
        matches = dict(
            kappa=re.search(kappa_pattern, cfun_path),
            kd=re.search(kd_pattern, cfun_path),
            shift=re.search(shift_pattern, cfun_path),
            source=re.search(source_pattern, cfun_path),
            sink=re.search(sink_pattern, cfun_path),
            configID=re.search(configID_pattern, cfun_path),
            operator=re.search(operator_pattern, cfun_path),
            structure=re.search(structure_pattern, cfun_path),
        )
        return {key: val.group(1) for key, val in matches.items() if val is not None}


def LoadSingleCorrelator(filename: str, dtype: str = ">c16") -> np.ndarray:
    """Loads a single correlator into a numpy array."""
    fullCorrelator = np.fromfile(filename, dtype=dtype)
    return fullCorrelator


def WriteSingleCorrelator(
    filename: str, correlator: np.ndarray, swapEndian: bool = True
):
    """Writes a single correlator from a numpy array to file."""
    if swapEndian is True:
        correlator.byteswap().tofile(filename)
    else:
        correlator.toFile(filename)


def LoadCorrelators(correlatorList: list, dtype: str = ">c16") -> np.ndarray:
    """
    Loads a list of correlators into a numpy array.

    Return array dimensions: [1:correlator_size , 1:num_correlators]
    """

    # Allocating array for correlators. Need to know if correlators are
    # mesons or baryons. Determine based on file size.

    # Size of first correlator in bytes
    size = Path(correlatorList[0]).stat().st_size
    if size == 16384:  # Baryon 2pt: 1024 complex elements
        array = np.zeros([1024, len(correlatorList)], dtype=dtype)
    elif size == 1024:  # Meson 2pt: 64 complex elements
        array = np.zeros([64, len(correlatorList)], dtype=dtype)
    else:
        raise ValueError(f"Correlator size: {size} bytes not supported")

    # Loading correlators
    for i, correlator in enumerate(correlatorList):
        # Checking all correlators are same size
        if Path(correlator).stat().st_size != size:
            raise ValueError("Correlators in correlatorList are not all same size.")
        # Loading correlator
        array[:, i] = LoadSingleCorrelator(correlator, dtype=dtype)
    return array


def AverageCorrelators(correlators: np.ndarray) -> np.ndarray:
    """
    Averages correlators in input array.

    Averages across last dimension. So correlators may be any shape,
    but last index of array must differentiate correlators.
    """
    arrayShape = np.shape(correlators)
    averageDimension = len(arrayShape) - 1  # -1 because python indexes from 0
    average = np.mean(correlators, axis=averageDimension)
    return average
