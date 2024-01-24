import os
from pathlib import Path
import re

import numpy as np

from utilities import configIDs as cfg, misc

# Regex patterns for parsing cfun_paths
tommi_patterns = dict(
    kappa = re.compile(r"\/k(13\d{3})\/"),
    kd = re.compile(r"\/BF([-+]?\d)\/"),
    shift = re.compile(r"\/sh(([xyzt]\d+)+|(None))\/"),
    source = re.compile(r"SO((sm|lp)\d+)"),
    sink = re.compile(r"si((sm|lp|ln)\d+)"),
    configID = re.compile(r"icfg(-(?:[ab]|[ghijk]M){1}-\d+)"),
    operator = re.compile(r"([\w\d_]+bar)_"),
    structure = re.compile(r"_([udsnlh]+)."),
)
liam_patterns = dict(
    kappa = re.compile(r"\/(13\d{3})\/"),
    shift = re.compile(r"\/(([xyzt]\d+)+|(None))\/"),
    source = re.compile(r"\/so((sm|lp)\d+)\/"),
    sink = re.compile(r"si((sm|lp|ln)\d+)"),
    configID = re.compile(r"icfg(-(?:[ab]|[ghijk]M){1}-\d+)"),
    operator = re.compile(r"([\w\d_]+bar)\."),
)
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

    def __repr__(self):
        return self.full_string

class CfunMetadata:
    # If cfun name structure changes, the regex at the
    # top of this file will likely need to change.
    def __init__(self, cfun_path: os.PathLike, regex_patterns: dict[str, re.Pattern] = tommi_patterns, **kwargs):
        """
        Class to hold the metadata for correlation functions.

        Constructed from a path to a correlation function using
        regex pattern matching. Key word arguments are included as
        extra metadata properties.

        Parameters
        ----------
        cfun_path : os.PathLike
            Full path to the correlation function.
        regex_patterns : dict[str, re.Pattern]
            Pattern set to use to parse properties from the cfun path.
        """
        for prop, val in kwargs.items():
            if prop in ("kd", "kappa"):
                val = int(val)
            setattr(self, prop, val)

        for prop, val in self.parse_cfun_path(cfun_path, regex_patterns).items():
            if prop in ("kd", "kappa"):
                val = int(val)
            setattr(self, prop, val)
            
        self.cfun_path = cfun_path

    @staticmethod
    def parse_cfun_path(cfun_path: os.PathLike, regex_patterns: dict[str, re.Pattern] = tommi_patterns) -> dict:
        """Parses a correlation function using regex. Expected form of the correlation function for tommi_patterns:
        /scratch/e31/tk9944/WorkingStorage/PhDRunThree/k13781/BF1/cfuns/shx23y08z26t00/SOsm250_icfg-kM-001630silp96.cascade0_1cascade0_1bar_uds.u.2cf
        
        For differently formatted correlators, pass a different pattern set."""
        
        # Use search so that we can obtain only the capturing group
        matches = {}
        for prop, pattern in regex_patterns.items():
            matches[prop] = re.search(pattern, cfun_path)

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


def LoadCorrelators(correlatorList: list, dtype: str = ">c16", transpose: bool = False) -> np.ndarray:
    """
    Loads a list of correlators into a numpy array.

    Return array dimensions: [1:correlator_size , 1:num_correlators]
     - Transposed if transpose = True
    """

    # Size of first correlator in bytes
    size = Path(correlatorList[0]).stat().st_size
    if size not in (262144, 16384, 1024):
        raise ValueError(f"Correlator size: {size} bytes not supported")

    # Double precision complex is 16 bytes
    dimensions = [len(correlatorList), size // 16] if transpose else [size // 16, len(correlatorList)]
    array = np.zeros(dimensions, dtype=dtype)

    # Loading correlators
    for i, correlator in enumerate(correlatorList):
        if i%1000 == 0:
            print(f"Loading {i+1}st of {len(correlatorList)} correlators")
        # Checking all correlators are same size
        if Path(correlator).stat().st_size != size:
            raise ValueError("Correlators in correlatorList are not all same size.")
        
        # Loading correlator
        if transpose:
            array[i, :] = LoadSingleCorrelator(correlator, dtype=dtype)
        else:
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
