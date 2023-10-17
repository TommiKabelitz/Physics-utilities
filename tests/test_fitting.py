import unittest

from utilities import fitting
from utilities import structure


class Test_calculate_landau(unittest.TestCase):
    def test_baryons(self):
        uds = structure.Structure("uds")
        self.assertAlmostEqual(
            fitting.PolarisabilityFit.calculate_landau(
                1.053819, "proton_1", uds, 0.0951
            ),
            0.037603,
            places=5,
        )
        self.assertAlmostEqual(
            fitting.PolarisabilityFit.calculate_landau(
                1.053819, "neutron_1", uds, 0.0951
            ),
            0,
            places=5,
        )


# class Test_convert_fit(unittest.TestCase):
#     def test_convert(self):
#         self.assertAlmostEqual(fitting.PolarisabilityFit.convert_fit(-0.0098517844, kappa=13700),0.000234630)
