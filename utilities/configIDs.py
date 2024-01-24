import re

runID_pattern = re.compile(r"(a|b|gM|hM|iM|jM|kM)")

# Functions holding the details for each ensemble. 
# Could really just be one dict but when I wrote it
# a long time ago I used functions because I was dumb.
# Now I can't be bothered fixing it

# 13700
def _k_13700():
    """_
    Hea_viest PACS-CS ensemble.
    kap_pa: 13700
    m_pi:  701 MeV
    a:     0.1022 fm
    """
    return {
        "kappa": 13700,
        "prefixes": ("b"),
        "m_pi": 701,
        "m_pi_phys": 623,
        "a": 0.1022,
        "traj_store": 10,
        "tau": 0.5,
        "rho": None,
        "N_poly": 180,
        "replay": "on",
    }


# 13727
def _k_13727():
    """
    Second heaviest PACS-CS ensemble.
    kappa: 13727
    m_pi:  570 MeV
    a:     0.10086 fm
    """
    return {
        "kappa": 13727,
        "prefixes": ("b"),
        "m_pi": 570,
        "m_pi_phys": 515,
        "a": 0.10086,
        "traj_store": 10,
        "tau": 0.5,
        "rho": None,
        "N_poly": 180,
        "replay": "on",
    }


# 13754
def _k_13754():
    """
    Middle PACS-CS ensemble.
    kappa: 13754
    m_pi:  411 MeV
    a:     0.0961 fm
    """
    return {
        "kappa": 13754,
        "prefixes": ("a", "b"),
        "m_pi": 411,
        "m_pi_phys": 391,
        "a": 0.0961,
        "traj_store": 10,
        "tau": 0.5,
        "rho": None,
        "N_poly": 180,
        "replay": "on",
    }


# 13770
def _k_13770():
    """
    Second lightest PACS-CS ensemble.
    kappa: 13770
    m_pi:  296 MeV
    a:     0.0951 fm
    """
    return {
        "kappa": 13770,
        "prefixes": ("a", "b"),
        "m_pi": 296,
        "m_pi_phys": 280,
        "a": 0.0951,
        "traj_store": 10,
        "tau": 0.25,
        "rho": None,
        "N_poly": 180,
        "replay": "on",
    }


# 13781
def _k_13781():
    """
    Lightest PACS-CS ensemble. 5 runs, 198 total configurations
    kappa: 13781
    m_pi:  156 MeV
    a:     0.0933 fm
    """
    return {
        "kappa": 13781,
        "prefixes": ("gM", "hM", "iM", "jM", "kM", "M"),
        "m_pi": 156,
        "m_pi_phys": 169,
        "a": 0.0933,
        "traj_store": 20,
        "tau": 0.5,
        "rho": 0.995,
        "N_poly": 200,
        "replay": "off",
    }


# Deprecated - but still can be used in cola
# # 12400
# def _k_12400():
#     """
#     This is for free field testing, the start point and number of configurations are arbitrary as
#     there are no configuration files here. COLA will simply generate the 'gauge field' in this case.
#     """
#     start = 1000
#     ncon = 5
#     return {"start": start, "ncon": ncon}


def _config_details(kappa: int) -> dict:
    """
    Get the details of the PACS configuration.

    Returns
    -------
    dict
        Dictionary of configuration details.
    """
    switch = {
        13700: _k_13700,
        13727: _k_13727,
        13754: _k_13754,
        13770: _k_13770,
        13781: _k_13781,
    }
    case = switch[kappa]
    return case()


startIDs_13781 = {
    1: "gM",
    45: "hM",
    67: "iM",
    111: "jM",
    155: "kM",
    199: "end",
}  # Just easier to add the end point to the dict

def runIDs_13781(ith_config: int) -> str:
    """Return the run ID associated with a configuration at 13781
    when all runs are chained together from 1 -> 198."""
    starts = startIDs_13781.keys()
    for previous_start, this_start in zip(starts[:-1], starts[1:]):
        if this_start > ith_config:
            return startIDs_13781[previous_start]
    else:
        raise ValueError("Somehow reached end of loop through 13781 IDs")


class ConfigID:
    def __init__(
        self, kappa: int, *, ID_str: str = None, icon: int = None, runID: str = None
    ):
        """
        Class to hold information about a specific configuration ID.

        Can be initialised from various combintations of information. Redundant information is cross-checked. Class is hashable so may be used in sets, dict keys.

        Parameters
        ----------
        kappa : int
            Kappa value of the configuration
        ID_str : str, optional
            The actual ConfigID string as placed in the config filename. If missing, icon and runID are required, by default None
        icon : int, optional
            The ith configuration which this ConfigID represents, by default None
        runID : str, optional
            The identifier for the Monte Carlo run, eg. a, b, gM,... , by default None
        """
        self.kappa = kappa
        # Initialise ensemble which requires runID
        if runID is None:
            if ID_str is None:
                raise ValueError(
                    "Require ID_str or icon and runID to initialise configID."
                )
            self.runID = self.get_runID(ID_str)
        else:
            self.runID = runID
        self.ensemble = PACSRun(self.kappa, self.runID)

        # Parse the ID string and verify its contents agree with the other passed info
        if ID_str is not None:
            self.ID_str = ID_str
            self.icon = self.ensemble.get_icon(self.ID_str)
            if icon not in (None, self.icon):
                raise ValueError(
                    "Mismatch between passed {icon = }, {ID_str = } and {kappa = }."
                )
            elif self.runID not in self.ID_str:
                raise ValueError("{runID = } not in {ID_str = }.")
        elif None in (icon, runID):
            raise ValueError(
                "Cannot initialise configID. Require ID string or both of icon and runID."
            )
        else:
            self.icon = icon
            self.ID_str = self.ensemble.get_ID_str(self.icon)

    @property
    def filename(self):
        return self.ensemble.filename(self)

    def __str__(self):
        return self.ID_str

    def __int__(self):
        return self.icon

    def __repr__(self):
        return f"{self.icon:3} {self.ID_str}"

    # Next three are required so that we can use ConfigIDs as dict keys
    def __hash__(self):
        return hash((self.icon, self.runID, self.kappa))

    def __eq__(self, other):
        return (self.icon, self.runID, self.kappa) == (
            other.icon,
            other.runID,
            other.kappa,
        )

    def __neq__(self, other):
        return not (self == other)

    @staticmethod
    def get_runID(ID_str: str) -> str:
        return runID_pattern.search(ID_str)[0]


class PACSEnsemble:
    base_filename = "RCNF2+1/RC32x64_B1900Kud0{kappa}00Ks01364000C1715/RC32x64_B1900Kud0{kappa}00Ks01364000C1715{ID_str}"

    def __init__(self, kappa: int):
        """
        Object for holding information about a specific PACS-CS ensemble. 
        Direct access to specific ensemble objects should use the PACS_ensembles dictionary instead to avoid creating many idential copies of this object.

        https://www.jldg.org/ildg-data/PACSCSconfig.html
        """

        details = _config_details(kappa)
        for detail, value in details.items():
            setattr(self, detail, value)

        self.kappa = kappa
        self.NS = 32
        self.NT = 64
        self.C_SW = 1.715
        self.beta = 1.9
        self.kappa_strange = 13640


class PACSRun:
    def __init__(self, kappa: int, runID: str):
        """
        Extension of the PACSEnsemble object for interacting with
        actual config IDs. Requires specification of runID.

        Access to all PACSEnsemble properties directly as attributes 
        of this class. The PACSEnsemble classes are pre-initialised and all
        instances of this class will point to the same object(s).
        
        RunID 'M' is available at 13781 for simplicity of accessing all
        configurations.

        Parameters
        ----------
        kappa : int
            Kappa value of the ensemble of interest
        runID : str
            The runID. eg 'a', 'b', 'hM', 'M' also available.
        """
        self.ensemble = PACS_ensembles[kappa]
        self.runID = runID
        self.start, self.ncon = self._get_run_details(kappa, runID)

    # TODO: Add this for M
    def get_icon(self, ID_str: str):
        """Extract the ith configuration number from a configuration string."""
        
        if self.runID == "M":
            raise NotImplementedError("Finding icon with runID set as M not supported.")
        
        num_ID = int(ID_str[-4:])
        icon = (num_ID - self.start) / self.traj_store + 1
        if icon > self.ncon:
            raise ValueError(f"{ID_str = } does not exist at {self.kappa = }.")
        return icon

    def get_ID_str(self, ith_config: int):
        """Form the configuration string corresponding to the ensembles ith configuration."""
        
        if self.runID == "M":
            trueID = runIDs_13781(ith_config)
            return PACSRun(13781, trueID).get_ID_str(ith_config)
        
        num_ID = self.start + (ith_config - 1) * self.traj_store
        return f"-{self.runID}-{num_ID:06}"

    def filename(self, configID: ConfigID) -> str:
        """Construct the file name corresponding to a particular config ID."""
        return self.base_filename.format(kappa=self.kappa, ID_str=configID.ID_str)

    @staticmethod
    def _get_run_details(kappa: int, runID: str):
        try:
            return PACS_run_details[int(kappa)][runID]
        except KeyError:
            raise ValueError("f{kappa = }, {runID = } is an invalid combination")
        
    # If cannot find an attribute, check the ensemble
    def __getattr__(self, attr):
        try:
            return getattr(self.ensemble,attr)
        except AttributeError:
            raise AttributeError(f"PACSRun has no attribute {attr}")


# Dictionary for accessing the PACS ensembles. Otherwise the objects would be
# needlessly created every time a ConfigID object is created
PACS_ensembles = {
    13700: PACSEnsemble(13700),
    13727: PACSEnsemble(13727),
    13754: PACSEnsemble(13754),
    13770: PACSEnsemble(13770),
    13781: PACSEnsemble(13781),
}


PACS_run_details = {
    13700: {"b": (2510, 400)},
    13727: {"b": (1310, 400)},
    13754: {"a": (2510, 200), "b": (2510, 250)},
    13770: {"a": (1880, 400), "b": (1780, 400)},
    13781: {
        "gM": (1200, 44),
        "hM": (1240, 22),
        "iM": (870, 44),
        "jM": (260, 44),
        "kM": (1090, 44),
        "M": (1200, 198),
    },
}
