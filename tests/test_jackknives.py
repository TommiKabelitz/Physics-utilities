import unittest

import numpy as np

from utilities import jackknives as jack


class Test_Jackknives(unittest.TestCase):
    def test_init(self):
        ensemble = jack.JackknifeEnsemble([1, 1.01, 0.99, 0.95, 1.05])
        self.assertAlmostEqual(ensemble.ensemble_average, 1)
        self.assertAlmostEqual(ensemble.jackknife_error, 0.0806, places=4)

    def test_addition(self):
        ensemble1 = jack.JackknifeEnsemble([1, 1.01, 0.99, 0.95, 1.05])
        ensemble2 = jack.JackknifeEnsemble([1, 1.01, 0.99, 0.95, 1.05])
        ensemble3 = ensemble1 + ensemble2
        self.assertAlmostEqual(ensemble3.ensemble_average, 2)
        self.assertAlmostEqual(ensemble3.jackknife_error, 0.16127, places=4)
        self.assertAlmostEqual((ensemble1 + 1).ensemble_average, 2)
        self.assertAlmostEqual((ensemble1 + 1).jackknife_error, 0.0806, places=4)

    def test_subtraction(self):
        ensemble1 = jack.JackknifeEnsemble([1, 1.01, 0.99, 0.95, 1.05])
        ensemble2 = jack.JackknifeEnsemble([2, 2.02, 1.98, 1.9, 2.1])
        ensemble3 = ensemble1 - ensemble2
        self.assertAlmostEqual(ensemble3.ensemble_average, -1)
        self.assertAlmostEqual(ensemble3.jackknife_error, 0.0806, places=4)
        self.assertAlmostEqual((ensemble1 - 1).ensemble_average, 0)
        self.assertAlmostEqual((ensemble1 - 1).jackknife_error, 0.0806, places=4)

    def test_multiplication(self):
        ensemble1 = jack.JackknifeEnsemble([1, 1.01, 0.99, 0.95, 1.05])
        ensemble2 = jack.JackknifeEnsemble([1, 1.01, 0.99, 0.95, 1.05])
        ensemble3 = ensemble1 * ensemble2
        self.assertAlmostEqual(ensemble3.ensemble_average, 1.0010, places=4)
        self.assertAlmostEqual(ensemble3.jackknife_error, 0.16127, places=4)
        self.assertAlmostEqual((ensemble1 * 2).ensemble_average, 2)
        self.assertAlmostEqual((ensemble1 * 2).jackknife_error, 0.16127, places=4)

    def test_division(self):
        ensemble1 = jack.JackknifeEnsemble([1, 1.01, 0.99, 0.95, 1.05])
        ensemble2 = jack.JackknifeEnsemble([1, 1.01, 0.99, 0.95, 1.05])
        ensemble3 = ensemble1 / ensemble2
        self.assertAlmostEqual(ensemble3.ensemble_average, 1)
        self.assertAlmostEqual(ensemble3.jackknife_error, 0, places=4)
        self.assertAlmostEqual((ensemble1 / 2).ensemble_average, 0.5)
        self.assertAlmostEqual((ensemble1 / 2).jackknife_error, 0.0403, places=4)
        self.assertAlmostEqual((1 / ensemble1).ensemble_average, 1.00104, places=4)
        self.assertAlmostEqual((1 / ensemble1).jackknife_error, 0.08087, places=4)

    def test_power(self):
        ensemble1 = jack.JackknifeEnsemble([1, 1.01, 0.99, 0.95, 1.05])
        ensemble2 = jack.JackknifeEnsemble([1, 1.01, 0.99, 0.95, 1.05])
        ensemble3 = ensemble1**ensemble2
        self.assertAlmostEqual(ensemble3.ensemble_average, 1.00104, places=4)
        self.assertAlmostEqual(ensemble3.jackknife_error, 0.08077, places=4)
        self.assertAlmostEqual((ensemble1**2).ensemble_average, 1.0010, places=4)
        self.assertAlmostEqual((ensemble1**2).jackknife_error, 0.16127, places=4)
        self.assertAlmostEqual((2**ensemble1).ensemble_average, 2.0004997, places=4)
        self.assertAlmostEqual((2**ensemble1).jackknife_error, 0.111797, places=4)

    def test_get_jackknives(self):
        data = np.array([1, 1.01, 0.99, 0.95, 1.05])
        jackknives = jack.JackknifeEnsemble.get_jackknives(data)
        self.assertTrue(
            np.isclose(
                jackknives, [1.0000, 0.9975, 1.0025, 1.0125, 0.9875], atol=1e-4
            ).all()
        )

    def test_get_jackknives_multidim(self):
        # fmt: off
        data = np.array(
            [[ 1.0, 1.01, 0.99, 0.95, 1.0500],
             [ 1.0, 2.0,  1.5,  0.95, 1.2   ],
             [-0.1, 1.3,  0.7,  0.2, -1.1001]]
        )
        result = np.array(
            [[1.0,     0.9975, 1.0025, 1.0125, 0.9875],
             [1.4125,  1.1625, 1.2875, 1.425,  1.3625],
             [ 0.275, -0.075,  0.075,  0.2,    0.525]]
        )
        # fmt: on
        self.assertTrue(
            np.isclose(jack.JackknifeEnsemble.get_jackknives(data,axis=1), result, atol=1e-4).all()
        )

    def test_init_from_data(self):
        # fmt: off
        data = np.array(
            [[ 1.0, 1.01, 0.99, 0.95, 1.0500],
             [ 1.0, 2.0,  1.5,  0.95, 1.2   ],
             [-0.1, 1.3,  0.7,  0.2, -1.1001]]
        )
        result = np.array(
            [[1.0,     0.9975, 1.0025, 1.0125, 0.9875],
             [1.4125,  1.1625, 1.2875, 1.425,  1.3625],
             [ 0.275, -0.075,  0.075,  0.2,    0.525]]
        )
        jackknife_errors = np.array([0.016125, 0.193391, 0.402492])
        j = jack.JackknifeEnsemble.init_jackknives_from_data(data, axis=1)
        self.assertTrue(np.isclose(j.jackknives, result, atol=1e-4).all())
        self.assertTrue(np.isclose(j.jackknife_error, jackknife_errors, atol=1e-4).all())