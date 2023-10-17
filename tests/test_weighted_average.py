from pathlib import Path
import unittest

import numpy as np
import pandas as pd


from utilities import weighted_average

data_file = Path(__file__).parents[0] / "data" / "weighted_avg.csv"


class Test_WeightedAverage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = pd.read_csv(data_file)
        cls.data["var_1"] = cls.data["ferr_1"] ** 2
        cls.data["var_2"] = cls.data["ferr_2"] ** 2

    def test_weighted_average(self):
        average = weighted_average.WeightedAverage(
            self.data,
            value_col_labels=["fmass_1", "fmass_2"],
            var_col_labels=["var_1", "var_2"],
        )
        values = average.do_average()
        np.testing.assert_allclose(average.weights, self.data["weight"])
        np.testing.assert_allclose(average.p_values, self.data["pvalue"])
        # More tests to write here
