import re

runID_pattern = re.compile(r"(a|b|gM|hM|iM|jM|kM)")


# 13700
def _k_13700(runPrefix):
    """_
    Hea_viest PACS-CS ensemble.
    kap_pa: 13700
    m_p_i:  701 MeV
    a:     0.1022 fm
    """
    if runPrefix == "b":
        start = 2510
        ncon = 400  # Technically 399 as one 4300 does not exist
    else:
        raise ValueError("Invalid (kappa,prefix) combination. Terminating")
    return {
        "kappa": 13700,
        "m_pi": 701,
        "a": 0.1022,
        "start": start,
        "ncon": ncon,
        "traj_store": 10,
        "tau": 0.5,
        "rho": None,
        "N_poly": 180,
        "replay": "on",
    }


# 13727
def _k_13727(runPrefix):
    """
    Second heaviest PACS-CS ensemble.
    kappa: 13727
    m_pi:  570 MeV
    a:     0.10086 fm
    """
    if runPrefix == "b":
        start = 1310
        ncon = 400
    else:
        raise ValueError("Invalid (kappa,prefix) combination. Terminating")
    return {
        "kappa": 13727,
        "m_pi": 570,
        "a": 0.10086,
        "start": start,
        "ncon": ncon,
        "traj_store": 10,
        "tau": 0.5,
        "rho": None,
        "N_poly": 180,
        "replay": "on",
    }


# 13754
def _k_13754(runPrefix):
    """
    Middle PACS-CS ensemble.
    kappa: 13754
    m_pi:  411 MeV
    a:     0.0961 fm
    """
    if runPrefix == "a":
        start = 2510
        ncon = 200
    elif runPrefix == "b":
        start = 2510
        ncon = 250
    else:
        raise ValueError("Invalid (kappa,prefix) combination. Terminating")
    return {
        "kappa": 13754,
        "m_pi": 411,
        "a": 0.0961,
        "start": start,
        "ncon": ncon,
        "traj_store": 10,
        "tau": 0.5,
        "rho": None,
        "N_poly": 180,
        "replay": "on",
    }


# 13770
def _k_13770(runPrefix):
    """
    Second lightest PACS-CS ensemble.
    kappa: 13770
    m_pi:  296 MeV
    a:     0.0951 fm
    """
    if runPrefix == "a":
        start = 1880
        ncon = 400
    elif runPrefix == "b":
        start = 1780
        ncon = 400
    else:
        raise ValueError("Invalid (kappa,prefix) combination. Terminating")
    return {
        "kappa": 13770,
        "m_pi": 296,
        "a": 0.0951,
        "start": start,
        "ncon": ncon,
        "traj_store": 10,
        "tau": 0.25,
        "rho": None,
        "N_poly": 180,
        "replay": "on",
    }


# 13781
def _k_13781(runPrefix):
    """
    Lightest PACS-CS ensemble. 5 runs, 198 total configurations
    kappa: 13781
    m_pi:  156 MeV
    a:     0.0933 fm
    """
    if runPrefix == "gM":
        start = 1200
        ncon = 44
    elif runPrefix == "hM":
        start = 1240
        ncon = 22
    elif runPrefix == "iM":
        start = 870
        ncon = 44
    elif runPrefix == "jM":
        start = 260
        ncon = 44
    elif runPrefix == "kM":
        start = 1090
        ncon = 44
    else:
        raise ValueError("Invalid (kappa,prefix) combination. Terminating")
    return {
        "kappa": 13781,
        "m_pi": 156,
        "a": 0.0933,
        "start": start,
        "ncon": ncon,
        "traj_store": 20,
        "tau": 0.5,
        "rho": 0.995,
        "N_poly": 200,
        "replay": "off",
    }


# 12400
def _k_12400(runPrefix):
    """
    This is for free field testing, the start point and number of configurations are arbitrary as
    there are no configuration files here. COLA will simply generate the 'gauge field' in this case.
    """
    start = 1000
    ncon = 5
    return {"start": start, "ncon": ncon}


def _config_details(kappa: int, runID: str) -> dict:
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
        12400: _k_12400,
    }
    case = switch[kappa]
    return case(runID)


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
        self.ensemble = PACS_ensembles[self.kappa][self.runID]

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

    def __init__(self, kappa: int, runID: str):
        """
        Object for holding information about a specific PACS-CS ensemble. Also contains methods for obtaining configIDs. Direct access to specific ensemble objects should use the PACS_ensembles dictionary instead.

        https://www.jldg.org/ildg-data/PACSCSconfig.html
        """

        details = _config_details(kappa, runID)
        for detail, value in details.items():
            setattr(self, detail, value)

        self.kappa = kappa
        self.runID = runID
        self.NS = 32
        self.NT = 64
        self.C_SW = 1.715
        self.beta = 1.9
        self.kappa_strange = 13640

    def get_icon(self, ID_str: str):
        """Extract the ith configuration number from a configuration string."""
        num_ID = int(ID_str[-4:])
        icon = (num_ID - self.start) / self.traj_store + 1
        if icon > self.ncon:
            raise ValueError(f"{ID_str = } does not exist at {self.kappa = }.")
        return icon

    def get_ID_str(self, ithConfig: int):
        """Form the configuration string corresponding to the ensembles ith configuration."""
        num_ID = self.start + (ithConfig - 1) * self.traj_store
        return f"-{self.runID}-{num_ID:06}"

    def filename(self, configID: ConfigID) -> str:
        """Construct the file name corresponding to a particular config ID."""
        return self.base_filename.format(kappa=self.kappa, ID_str=configID.ID_str)


# Dictionary for accessing the PACS ensembles. Otherwise the objects would be
# needlessly created every time a ConfigID object is created
PACS_ensembles = {
    13700: {"b": PACSEnsemble(13700, "b")},
    13727: {"b": PACSEnsemble(13727, "b")},
    13754: {"a": PACSEnsemble(13754, "a"), "b": PACSEnsemble(13754, "b")},
    13770: {"a": PACSEnsemble(13770, "a"), "b": PACSEnsemble(13770, "b")},
    13781: {
        "gM": PACSEnsemble(13781, "gM"),
        "hM": PACSEnsemble(13781, "hM"),
        "iM": PACSEnsemble(13781, "iM"),
        "jM": PACSEnsemble(13781, "jM"),
        "kM": PACSEnsemble(13781, "kM"),
    },
}
