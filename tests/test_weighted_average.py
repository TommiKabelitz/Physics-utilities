from pathlib import Path
import unittest

import gvar as gv
import numpy as np
import pandas as pd


from utilities import weighted_average

data_file = Path(__file__).parents[0] / "data" / "weighted_avg.csv"


class Test_WeightedAverage(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.data = pd.read_csv(data_file)
        self.data["var_1"] = self.data["ferr_1"] ** 2
        self.data["var_2"] = self.data["ferr_2"] ** 2
        self.average = weighted_average.WeightedAverage(
            self.data,
            err_label="ferr_1",
            value_col_labels=["fmass_1", "fmass_2"],
            var_col_labels=["var_1", "var_2"],
        )
        self.values = self.average.do_average()
        self.reference_values = [gv.gvar("0.01386123(85837)"), gv.gvar("0.01143814(216822)")]


    def test_init(self):
        average = weighted_average.WeightedAverage(
            self.data,
            err_label="ferr_1",
            value_col_labels=["fmass_1", "fmass_2"],
            var_col_labels=["var_1", "var_2"],
        )
        average.do_average()
        
    def test_p_values(self):
        np.testing.assert_allclose(self.average.p_values, self.data["p_value"])
        
    def test_weights(self):
        np.testing.assert_allclose(self.average.weights, self.data["weight"])
        
    def test_result(self):
        np.testing.assert_allclose(gv.mean(self.values), gv.mean(self.reference_values), rtol=5.0e-6)
        np.testing.assert_allclose(gv.sdev(self.values), gv.sdev(self.reference_values), rtol=5.0e-6)

        
        
        
