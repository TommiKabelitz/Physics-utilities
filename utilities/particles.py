"""
Module of particle operators to be used.

Added particles should follow the same format as those already
present. Particles with multiple terms in their interpolating
field should have each term added as an item in a list.

There are also a couple of utility functions at the bottom
QuarkCharge, HadronicCharge

"""
from utilities import structure

Structure = structure.Structure
########################################Baryons


# Currently implemented octet baryons with _1,_2 denoting
# which of the two possible interpolating fields is used.
# Particle charge is denoted by 0 (neutral), p (+1),
# m (-1).
# ie. sigmap is a sigma+, but + cannot be used
# in an object name.
# Would recommend deltapp for charge 2 particles such
# as the delta ++


class Particle:
    properties = [
        "composition",
        "interpolator_terms",
        "levi_civita_indices",
        "gell_mann_matrices",
        "lorentz_indices",
    ]

    def __init__(
        self,
        composition: list[str] = None,
        interpolator_terms: list[str] = None,
        levi_civita_indices: list[str] = None,
        gell_mann_matrices: list[str] = None,
        lorentz_indices: list[str] = None,
    ):
        if composition is interpolator_terms is None:
            raise ValueError("Need one of composition or interpolator terms.")
        elif composition is None:
            self.composition = self.get_quark_composition(interpolator_terms[0])
        else:
            self.composition = composition

        self.interpolator_terms = interpolator_terms
        self.levi_civita_indices = levi_civita_indices
        self.gell_mann_matrices = gell_mann_matrices
        self.lorentz_indices = lorentz_indices

    def __repr__(self):
        return "\n".join(
            [
                f"{attr} = {a}"
                for attr in self.properties
                if (a := getattr(self, attr)) is not None
            ]
        )

    @staticmethod
    def get_quark_composition(interpolator_term: str):
        all_quarks = {
            quark: interpolator_term.count(f"{quark}^") for quark in ["u", "d", "s"]
        }
        anti_quarks = {
            quark: interpolator_term.count(f"{quark}^") for quark in ["Au", "Ad", "As"]
        }

        for quark, anti_count in anti_quarks.items():
            all_quarks[quark[1:]] -= anti_count

        all_quarks = {**all_quarks, **anti_quarks}
        composition = []
        for quark, count in all_quarks.items():
            composition += [quark] * count
        return composition


proton_1 = Particle(
    levi_civita_indices=["a;b;c;"],
    interpolator_terms=["1.0/sqrt(2.0) * [u^{a} (C\gamma_{5}) d^{b}] (I) u^{c}"],
)


proton_1bar = Particle(
    levi_civita_indices=["ap;bp;cp;"],
    interpolator_terms=["-1.0/sqrt(2.0) * Au^{cp} (I) [Ad^{bp} (C\gamma_{5}) Au^{ap}]"],
)


sigmap_1 = Particle(
    levi_civita_indices=["a;b;c;"],
    interpolator_terms=["1.0/sqrt(2.0) * [u^{a} (C\gamma_{5}) s^{b}] (I) u^{c}"],
)


sigmap_1bar = Particle(
    levi_civita_indices=["ap;bp;cp;"],
    interpolator_terms=["-1.0/sqrt(2.0) * Au^{cp} (I) [As^{bp} (C\gamma_{5}) Au^{ap}]"],
)


sigmam_1 = Particle(
    levi_civita_indices=["a;b;c;"],
    interpolator_terms=["1.0/sqrt(2.0) * [d^{a} (C\gamma_{5}) s^{b}] (I) d^{c}"],
)


sigmam_1bar = Particle(
    levi_civita_indices=["ap;bp;cp;"],
    interpolator_terms=["-1.0/sqrt(2.0) * Ad^{cp} (I) [As^{bp} (C\gamma_{5}) Ad^{ap}]"],
)


neutron_1 = Particle(
    levi_civita_indices=["a;b;c;"],
    interpolator_terms=["1.0/sqrt(2.0) * [u^{a} (c\gamma_{5}) d^{b}] (i) d^{c}"],
)


neutron_1bar = Particle(
    levi_civita_indices=["ap;bp;cp;"],
    interpolator_terms=["-1.0/sqrt(2.0) * Ad^{cp} (I) [Ad^{bp} (C\gamma_{5}) Au^{ap}]"],
)


cascade0_1 = Particle(
    levi_civita_indices=["a;b;c;"],
    interpolator_terms=["1.0/sqrt(2.0) * [u^{a} (C\gamma_{5}) s^{b}] (I) s^{c}"],
)


cascade0_1bar = Particle(
    levi_civita_indices=["ap;bp;cp;"],
    interpolator_terms=["-1.0/sqrt(2.0) * As^{cp} (I) [As^{bp} (C\gamma_{5}) Au^{ap}]"],
)


cascadem_1 = Particle(
    levi_civita_indices=["a;b;c;"],
    interpolator_terms=["1.0/sqrt(2.0) * [d^{a} (C\gamma_{5}) s^{b}] (I) s^{c}"],
)


cascadem_1bar = Particle(
    levi_civita_indices=["ap;bp;cp;"],
    interpolator_terms=["-1.0/sqrt(2.0) * As^{cp} (I) [As^{bp} (C\gamma_{5}) Ad^{ap}]"],
)


proton_2 = Particle(
    levi_civita_indices=["a;b;c;"],
    interpolator_terms=["1.0/sqrt(2.0) * [u^{a} (C) d^{b}] (\gamma_{5}) u^{c}"],
)


proton_2bar = Particle(
    levi_civita_indices=["ap;bp;cp;"],
    interpolator_terms=["-1.0/sqrt(2.0) * Au^{cp} (\gamma_{5}) [Ad^{bp} (C) Au^{ap}]"],
)


sigmap_2 = Particle(
    levi_civita_indices=["a;b;c;"],
    interpolator_terms=["1.0/sqrt(2.0) * [u^{a} (C) s^{b}] (\gamma_{5}) u^{c}"],
)


sigmap_2bar = Particle(
    levi_civita_indices=["ap;bp;cp;"],
    interpolator_terms=["-1.0/sqrt(2.0) * Au^{cp} (\gamma_{5}) [As^{bp} (C) Au^{ap}]"],
)


sigmam_2 = Particle(
    levi_civita_indices=["a;b;c;"],
    interpolator_terms=["1.0/sqrt(2.0) * [d^{a} (C) s^{b}] (\gamma_{5}) d^{c}"],
)


sigmam_2bar = Particle(
    levi_civita_indices=["ap;bp;cp;"],
    interpolator_terms=["-1.0/sqrt(2.0) * Ad^{cp} (\gamma_{5}) [As^{bp} (C) Ad^{ap}]"],
)


neutron_2 = Particle(
    levi_civita_indices=["a;b;c;"],
    interpolator_terms=["1.0/sqrt(2.0) * [u^{a} (C) d^{b}] (\gamma_{5}) d^{c}"],
)


neutron_2bar = Particle(
    levi_civita_indices=["ap;bp;cp;"],
    interpolator_terms=["-1.0/sqrt(2.0) * Ad^{cp} (\gamma_{5}) [Au^{bp} (C) Ad^{ap}]"],
)


cascade0_2 = Particle(
    levi_civita_indices=["a;b;c;"],
    interpolator_terms=["1.0/sqrt(2.0) * [u^{a} (C) s^{b}] (\gamma_{5}) s^{c}"],
)


cascade0_2bar = Particle(
    levi_civita_indices=["ap;bp;cp;"],
    interpolator_terms=["-1.0/sqrt(2.0) * As^{cp} (\gamma_{5}) [Au^{bp} (C) As^{ap}]"],
)


cascadem_2 = Particle(
    levi_civita_indices=["a;b;c;"],
    interpolator_terms=["1.0/sqrt(2.0) * [d^{a} (C) s^{b}] (\gamma_{5}) s^{c}"],
)


cascadem_2bar = Particle(
    levi_civita_indices=["ap;bp;cp;"],
    interpolator_terms=["-1.0/sqrt(2.0) * As^{cp} (\gamma_{5}) [Ad^{bp} (C) As^{ap}]"],
)


# #####Mixing baryons


sigma0_1 = Particle(
    levi_civita_indices=["a;b;c;"],
    interpolator_terms=[
        "1.0/sqrt(2.0) * [u^{a} (C\gamma_{5}) s^{b}] (I) d^{c}",
        "1.0/sqrt(2.0) * [d^{a} (C\gamma_{5}) s^{b}] (I) u^{c}",
    ],
)


sigma0_1bar = Particle(
    levi_civita_indices=["ap;bp;cp;"],
    interpolator_terms=[
        "-1.0/sqrt(2.0) * Ad^{cp} (I) [As^{bp} (C\gamma_{5}) Au^{ap} ]",
        "-1.0/sqrt(2.0) * Au^{cp} (I) [As^{bp} (C\gamma_{5}) Ad^{ap} ]",
    ],
)


lambda0_1 = Particle(
    levi_civita_indices=["a;b;c;"],
    interpolator_terms=[
        "2.0/sqrt(6.0) * [u^{a} (C\gamma_{5}) d^{b} ] (I) s^{c}",
        "1.0/sqrt(6.0) * [u^{a} (C\gamma_{5}) s^{b} ] (I) d^{c}",
        "-1.0/sqrt(6.0) * [d^{a} (C\gamma_{5}) s^{b} ] (I) u^{c}",
    ],
)


lambda0_1bar = Particle(
    levi_civita_indices=["ap;bp;cp;"],
    interpolator_terms=[
        "-2.0/sqrt(6.0) * As^{cp} (I) [Ad^{bp} (C\gamma_{5}) Au^{ap} ]",
        "-1.0/sqrt(6.0) * Ad^{cp} (I) [As^{bp} (C\gamma_{5}) Au^{ap} ]",
        "1.0/sqrt(6.0) * Au^{cp} (I) [As^{bp} (C\gamma_{5}) Ad^{ap} ]",
    ],
)


# # DID THIS
sigma0_2 = Particle(
    lorentz_indices=[],
    gell_mann_matrices=[],
    levi_civita_indices=["a;b;c;"],
    interpolator_terms=[
        "1.0/sqrt(2.0) * [u^{a} (C) s^{b}] (\gamma_{5}) d^{c}",
        "1.0/sqrt(2.0) * [d^{a} (C) s^{b}] (\gamma_{5}) u^{c}",
    ],
)


sigma0_2bar = Particle(
    levi_civita_indices=["ap;bp;cp;"],
    interpolator_terms=[
        "-1.0/sqrt(2.0) * Ad^{cp} (\gamma_{5}) [As^{bp} (C) Au^{ap} ]",
        "-1.0/sqrt(2.0) * Au^{cp} (\gamma_{5}) [As^{bp} (C) Ad^{ap} ]",
    ],
)


lambda0_2 = Particle(
    levi_civita_indices=["a;b;c;"],
    interpolator_terms=[
        "2.0/sqrt(6.0) * [u^{a} (C) d^{b} ] (\gamma_{5}) s^{c}",
        "1.0/sqrt(6.0) * [u^{a} (C) s^{b} ] (\gamma_{5}) d^{c}",
        "-1.0/sqrt(6.0) * [d^{a} (C) s^{b} ] (\gamma_{5}) u^{c}",
    ],
)


lambda0_2bar = Particle(
    levi_civita_indices=["ap;bp;cp;"],
    interpolator_terms=[
        "-2.0/sqrt(6.0) * As^{cp} (\gamma_{5}) [Ad^{bp} (C) Au^{ap} ]",
        "-1.0/sqrt(6.0) * Ad^{cp} (\gamma_{5}) [As^{bp} (C) Au^{ap} ]",
        "1.0/sqrt(6.0) * Au^{cp} (\gamma_{5}) [As^{bp} (C) Ad^{ap} ]",
    ],
)


# ######################Mesons


pip = Particle(
    interpolator_terms=["1.0 * [Ad^{e} (\gamma_{5}) u^{e}]"],
)

pipbar = Particle(
    interpolator_terms=["-1.0 * [Au^{ep} (\gamma_{5}) d^{ep}"],
)

kaonp = Particle(
    interpolator_terms=["1.0 * [As^{e} (\gamma_{5}) u^{e}]"],
)

kaonpbar = Particle(
    interpolator_terms=["-1.0 * [Au^{ep} (\gamma_{5}) s^{ep}"],
)

# Actual utility functions


quark_charge = {
    "u": 2 / 3,
    "d": -1 / 3,
    "s": -1 / 3,
    "nl": 0,
    "nh": 0,
    "l": 0,
    "h": 0,
}


def get_particle_charge(particle: str | Particle, structure: Structure = None):
    if structure is None:
        structure = Structure("uds")

    if isinstance(particle, Particle):
        composition = particle.composition
    elif isinstance(particle, str):
        composition = globals()[particle].composition
    else:
        raise TypeError("particle must be str or Particle object.")

    struct_dict = structure.as_dict()
    charge = 0
    for quark in composition:
        if quark[0] == "A":
            sign = -1
            quark = quark[1:]
        else:
            sign = 1
        charge += sign * quark_charge[struct_dict[quark]]
    return charge


def CheckForVanishingFields(
    isospin_sym, particleList=None, chi=None, chibar=None, *args, **kwargs
):
    """
    Removes interpolator combinations which vanish under isospin sym.

    Arguments:
    isospin_sym -- bool: Whether isospin symmetry is true.
    particList  -- nested list: List of list of particle names. In form
                         [chi,chibar].

    Returns:
    updatedList -- nested list: List of list of particle names. Format as
                       above. Function does not act in place.
    """

    if isospin_sym is False:
        return particleList

    if particleList is None:
        if chi is None or chibar is None:
            raise ValueError(
                "Either particleList or chi and chibar must be specified with non-None values"
            )

        particleList = [[chi, chibar]]

    # Particles which when combined in any source/sink operator combination produce 0
    # with isospin symmetry should be placed here. Each inner list will test all
    # permutations of that list. Separate inner lists will not be compared.
    # ie. [[a,b,c],[d,e]] would check all permutations of ab,ac,ba... and de...
    # but not ad,ae...
    badParticles = [["lambda0", "sigma0"]]

    badCombinations = []
    # Getting the combinations which vanish. Assumes aa would not vanish
    for particleSet in badParticles:
        badCombinations.append(
            [[p1, p2] for p1 in particleSet for p2 in particleSet if p1 != p2]
        )
    # Un-nests the list so that we can just use 1 loop
    badCombinations = [comb for sublist in badCombinations for comb in sublist]

    # Looping through particles and bad combinations
    badList = []
    for chi, chibar in particleList:
        for pair in badCombinations:
            # Checking if the particles match
            if pair[0] in chi and pair[1] in chibar:
                badList.append([chi, chibar])

    # Don't want to modify the original list
    updatedList = particleList.copy()
    # Removing vanishing combinations
    for chi, chibar in badList:
        updatedList.remove([chi, chibar])

    return updatedList
