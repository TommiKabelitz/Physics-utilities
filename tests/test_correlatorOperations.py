import unittest

from utilities import correlatorOperations as co
from utilities import configIDs as cfg


class Test_CfunMetadata(unittest.TestCase):
    def test_init(self):
        cfun_path = "/scratch/e31/tk9944/WorkingStorage/PhDRunThree/k13781/BF1/cfuns/shx23y08z26t00/SOsm250_icfg-kM-001630silp96.cascade0_1cascade0_1bar_uds.u.2cf"
        cfun = co.CfunMetadata(cfun_path)
        self.assertEqual(cfun.kappa, 13781)
        self.assertEqual(cfun.kd, 1)
        self.assertEqual(cfun.shift, "x23y08z26t00")
        self.assertEqual(cfun.source, "sm250")
        self.assertEqual(cfun.sink, "lp96")
        self.assertEqual(cfun.configID, "-kM-001630")
        self.assertEqual(cfun.operator, "cascade0_1cascade0_1bar")
        self.assertEqual(cfun.structure, "uds")

    def test_init(self):
        cfun_path = "SOsm250_icfg-kM-001630silp96.cascade0_1cascade0_1bar_uds.u.2cf"
        cfun = co.CfunMetadata(cfun_path)
        self.assertEqual(cfun.source, "sm250")
        self.assertEqual(cfun.sink, "lp96")
        self.assertEqual(cfun.configID, "-kM-001630")
        self.assertEqual(cfun.operator, "cascade0_1cascade0_1bar")
        self.assertEqual(cfun.structure, "uds")
        
        
class Test_ExceptionalConfig(unittest.TestCase):
    def test_init(self):
        kappa = 13781
        shift = "x23y08z26t00"
        ID_str = "-kM-001630"
        as_str = f"{kappa} {ID_str} {shift}"
        exc = co.ExceptionalConfig(kappa, cfg.ConfigID(kappa, ID_str = ID_str), shift)
        self.assertEqual(exc.full_string, as_str)


    def test_init_from_str(self):
        kappa = 13781
        shift = "x23y08z26t00"
        ID_str = "-kM-001630"
        as_str = f"{kappa} {ID_str} {shift}"
        exc = co.ExceptionalConfig(kappa, cfg.ConfigID(kappa, ID_str = ID_str), shift)
        self.assertEqual(exc, co.ExceptionalConfig.init_from_string(as_str))
        