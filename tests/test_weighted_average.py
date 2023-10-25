from pathlib import Path
import unittest

import gvar as gv
import numpy as np
import pandas as pd


from utilities import weighted_average

data_file = Path(__file__).parents[0] / "data" / "weighted_avg.csv"


class Test_WeightedAverage_multifit(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.data = pd.read_csv(data_file)
        self.average = weighted_average.WeightedAverage_multifit(
            self.data,
            err_label="ferr_1",
            value_col_labels=["fmass_1", "fmass_2"],
            error_col_labels=["ferr_1", "ferr_2"],
        )
        self.values = self.average.do_average()
        self.reference_values = [gv.gvar("0.01386123(85837)"), gv.gvar("0.01143814(216822)")]


    def test_init(self):
        average = weighted_average.WeightedAverage_multifit(
            self.data,
            err_label="ferr_1",
            value_col_labels=["fmass_1", "fmass_2"],
            error_col_labels=["ferr_1", "ferr_2"],
        )
        average.do_average()
        
    def test_p_values(self):
        np.testing.assert_allclose(self.average.p_values, self.data["p_value"])
        
    def test_weights(self):
        np.testing.assert_allclose(self.average.weights, self.data["weight"])
        
    def test_result(self):
        np.testing.assert_allclose(gv.mean(self.values), gv.mean(self.reference_values), rtol=5.0e-6)
        np.testing.assert_allclose(gv.sdev(self.values), gv.sdev(self.reference_values), rtol=5.0e-6)


class Test_WeightedAverage(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.data = pd.read_csv(data_file)
        self.average = weighted_average.WeightedAverage(
            self.data,
            value_label="fmass_1",
            err_label="ferr_1",
        )
        self.value = self.average.do_average()
        self.reference_value = gv.gvar("0.01386123(85837)")


    def test_init(self):
        average = weighted_average.WeightedAverage(
            self.data,
            value_label="fmass_1",
            err_label="ferr_1",
        )
        average.do_average()
        
    def test_p_values(self):
        np.testing.assert_allclose(self.average.p_values, self.data["p_value"])
        
    def test_weights(self):
        np.testing.assert_allclose(self.average.weights, self.data["weight"])
        
    def test_result(self):
        np.testing.assert_allclose(gv.mean(self.value), gv.mean(self.reference_value), rtol=5.0e-6)
        np.testing.assert_allclose(gv.sdev(self.value), gv.sdev(self.reference_value), rtol=5.0e-6)

        
        
        
