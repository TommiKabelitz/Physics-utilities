import os
from pathlib import Path
import re

import numpy as np

from utilities import configIDs as cfg

# Regex patterns for parsing cfun_paths
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
        """
        Convenient class to hold details of exceptional configurations

        Initialised with the relevant kappa, configID and shift of an exceptional
        configuration. Contains methods for initialisation also from cfun_path and 
        from a string form which this class can also generate for easy permanent
        storage.

        Parameters
        ----------
        kappa : int
            The kappa value of the configuration
        configID : cfg.ConfigID
            A configID object containing the information about the configID
        shift : str
            The gauge shift of the configuration
        """
        self.kappa = kappa
        self.configID = configID
        self.shift = shift
        self._verify_init()

    # hash, eq, and neq allow use in sets, dict keys and also allows
    # comparison between configurations
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
        """Relevant information as a string. For file storage.
        eg. 13781 -kM-001670 x23y27z02t00"""
        return f"{self.kappa} {str(self.configID)} {self.shift}"

    @staticmethod
    def init_from_string(exceptional_string: str):
        """Init the class from a string in the form returned by
        ExceptionalConfig.full_string."""
        kappa, config_str, shift = exceptional_string.split(" ")
        configID = cfg.ConfigID(int(kappa), ID_str=config_str)
        return ExceptionalConfig(int(kappa), configID, shift)

    @staticmethod
    def init_from_cfun_path(cfun_path: os.PathLike, **kwargs):
        """
        Initialises the object from a full path to a correlation function.
        
        Uses the CfunMetadata constructor to parse the cfun, kwargs are passed
        to that constructor.
        """
        cfun = CfunMetadata(cfun_path, **kwargs)
        try:
            return ExceptionalConfig(
                cfun.kappa, cfg.ConfigID(cfun.kappa, ID_str=cfun.configID), cfun.shift
            )
        except AttributeError:
            raise ValueError(
                f"Could not extract kappa, configID and shift from {cfun_path=}."
            )

    
    def _verify_init(self):
        """Verify that kappa, configID and shift are set and not none"""
        for prop in ("kappa", "configID", "shift"):
            try:
                if getattr(self, prop) is None:
                    raise ValueError("Exceptional configuration initialisation failed, {prop} is None")
            except AttributeError:
                raise ValueError("Exceptional configuration initialisation failed, {prop} is unset")

class CfunMetadata:
    # If cfun name structure changes, the regex at the
    # top of this file will likely need to change.
    def __init__(self, cfun_path: os.PathLike, **kwargs):
        """
        Class to hold the metadata for correlation functions.

        Constructed from a path to a correlation function using
        regex pattern matching. Key word arguments are included as
        extra metadata properties.

        Parameters
        ----------
        cfun_path : os.PathLike
            Full path to the correlation function.
        """
        for prop, val in kwargs.items():
            if prop in ("kd", "kappa"):
                val = int(val)
            setattr(self, prop, val)
        for prop, val in self.parse_cfun_path(cfun_path).items():
            if prop in ("kd", "kappa"):
                val = int(val)
            setattr(self, prop, val)
            
        self.cfun_path = cfun_path

    @staticmethod
    def parse_cfun_path(cfun_path: os.PathLike) -> dict:
        """Parses a correlation function using regex. Expected form of the correlation function:
        /scratch/e31/tk9944/WorkingStorage/PhDRunThree/k13781/BF1/cfuns/shx23y08z26t00/SOsm250_icfg-kM-001630silp96.cascade0_1cascade0_1bar_uds.u.2cf"""
        
        # Use search so that we can obtain only the capturing group
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
        # The actual values are at location 1 in the groups, 0 is the full match
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
