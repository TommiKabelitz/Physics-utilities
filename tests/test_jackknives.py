import unittest

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
        ensemble3 = ensemble1 ** ensemble2
        self.assertAlmostEqual(ensemble3.ensemble_average, 1.00104, places=4)
        self.assertAlmostEqual(ensemble3.jackknife_error, 0.08077, places=4)
        self.assertAlmostEqual((ensemble1 ** 2).ensemble_average, 1.0010, places=4)
        self.assertAlmostEqual((ensemble1 ** 2).jackknife_error, 0.16127, places=4)
        self.assertAlmostEqual((2 ** ensemble1).ensemble_average, 2.0004997, places=4)
        self.assertAlmostEqual((2 ** ensemble1).jackknife_error, 0.111797, places=4)