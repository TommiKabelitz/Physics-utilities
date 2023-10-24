import logging

import gvar as gv
import numpy as np
import pandas as pd
from scipy.stats import gamma as gamma_dist
from scipy.special import gamma as gamma_fun

logger = logging.getLogger(__name__)
logging.Formatter(fmt="%(name)s(%(lineno)d)::%(levelname)-8s: %(message)s")


class WeightedAverage:
    def __init__(
        self,
        data: pd.DataFrame,
        value_col_labels: list[str],
        var_col_labels: list[str],
        err_label: str,
        chi2_label: str = "chi2",
        ndof_label: str = "ndof",
    ):
        """
        Class to determine the weighted average of some data given the values, VARIANCES, chi 
        squares and number of degrees of freedom. Based on arxiv.org/abs/2003.12130.`

        The weighted average uses the chi_square distribution to give fits p-values from which
        weights may be assigned. This interface allows an arbitrary number of datasets to be 
        averaged based on the same chisquare and n degrees of freedom for each dataset. The number 
        of values to be averaged is also arbitrary.

        Data should be formatted in a DataFrame with a column of chi^2 values and a column of 
        degrees of freedom. The actual values and variances must be further columns of the DataFrame.

        All column labels must be specified as arguments at initialisation. 
        The value and variance column labels are assumed to match elementwise.

        Parameters
        ----------
        data : pd.DataFrame
            The DataFrame holding the data as descibed above.
        value_col_labels : list[str]
            List of column labels where the actual values to average are located. The ith element
            of this list will be matched with the ith element of var_col_labels.
        var_col_labels : list[str]
            As value_col_labels but for the variances
        err_label : str
            The column label to use as the uncertainty for calculating the weights
        chi2_label : str, optional
            Column label for column holding chi square values. Note: not reduced chi square, by default "chi2"
        ndof_label : str, optional
            Column label for column holding degrees of freedom values, by default "ndof"

        Raises
        ------
        ValueError
            In case of length mismatch between value_col_labels and variance_col_labels
        """
        if len(value_col_labels) != len(var_col_labels):
            raise ValueError(
                "Length mismatch between value and variance column label lists."
            )
        self.data = data
        self.working_df = pd.DataFrame()
        self.labels = Labels(
            chi2=chi2_label,
            ndof=ndof_label,
            err=err_label,
            value_cols=value_col_labels,
            variance_cols=var_col_labels,
        )

    def do_average(self, recalculate_weights: bool = False) -> list[gv.GVar]:
        """
        Calculate the weighted average. A list of gvar variables is returned.

        Parameters
        ----------
        recalculate_weights : bool, optional
            Whether the weights should be re-calculated if they are already calculated, by default False

        Returns
        -------
        list[gv.GVar]
            The weighted average for each (value,variance) column pair.
        """

        if "weight" in self.working_df.columns and recalculate_weights is False:
            logging.warning(
                "Weights already calculated. Pass recalculate_weights=True to recalculate weights."
            )
        else:
            self.calculate_weights()

        logger.debug("Weights calculated, determining weighted average")
        values = []
        for val_col, var_col in zip(self.labels.value_cols, self.labels.variance_cols):
            logger.debug(f"Doing column pair {val_col}, ({var_col})")

            # Reweighted value, variance and systematic variance column labels
            re_val = f"{val_col}*w"
            re_var = f"{var_col}*w"
            re_var_sys = f"{var_col}_sys"

            # Reweighted values and variances
            self.working_df[re_val] = self.data[val_col] * self.working_df["weight"]
            self.working_df[re_var] = self.data[var_col] * self.working_df["weight"]

            weighted_average = self.working_df[re_val].sum()

            # Systematic error contribution from each row
            self.working_df[re_var_sys] = (
                self.working_df["weight"] * (self.data[val_col] - weighted_average) ** 2
            )

            # Summing uncertainty contributions and add systematic to systematic in quadrature
            stat_var = self.working_df[re_var].sum()
            sys_var = self.working_df[re_var_sys].sum()
            total_uncertainty = np.sqrt(stat_var + sys_var)
            result = gv.gvar(weighted_average, total_uncertainty)
            values.append(result)
            logger.debug(f"{result = }")

        return values

    def calculate_weights(self) -> np.ndarray:
        """
        Calculate the weights for each row. See documentation of the WeightedAverage class for implementation details on the weight calculation.

        Weights are returned in a vector and also added to the working DataFrame.

        Returns
        -------
        np.ndarray
            Array of weights.
        """

        logger.debug("Calculating weights")
        self.working_df["p_value"] = self.data.apply(self.df_p_value, axis=1)
        self.working_df["err"] = self.data[self.labels.err]
        normalisation = (self.working_df["err"] ** (-2) * self.working_df["p_value"]).sum()

        self.working_df["weight"] = self.working_df.apply(
            self.df_weight, axis=1, normalisation=normalisation
        )
        return self.working_df["weight"].to_numpy()

    @staticmethod
    def p_value(Ndof: int, chi_square: float) -> float:
        """Calculate p-value based on chi square distribution."""
        # chi square distribution is just gamma distribution re-scaled
        return gamma_dist.pdf(Ndof / 2, chi_square / 2) / gamma_fun(Ndof / 2)

    @staticmethod
    def weight(p_value: float, error: float, normalisation: float):
        """Calculate the relative weight based on the p_value and the normalisation."""
        return p_value * error ** (-2) / normalisation

    @staticmethod
    def df_p_value(df_row):
        """For applying p_value to a DataFrame"""
        return WeightedAverage.p_value(df_row["ndof"], df_row["chi2"])

    @staticmethod
    def df_weight(df_row, normalisation: float):
        """For applying weight to a DataFrame"""
        return WeightedAverage.weight(
            df_row["p_value"], df_row["err"], normalisation
        )

    @property
    def weights(self):
        try:
            return self.working_df["weight"]
        except KeyError:
            raise ValueError(
                "Weights not calculated yet. Call calculate_weights or do_average to calculate weights."
            )

    @property
    def p_values(self):
        try:
            return self.working_df["p_value"]
        except KeyError:
            raise ValueError(
                "P values not calculated yet. Call calculate_weights or do_average to calculate P values."
            )


class Labels:
    def __init__(
        self,
        chi2: str,
        ndof: str,
        err: str,
        value_cols: list[str],
        variance_cols: list[str],
    ):
        """Simple class to hold labels for the weighted averaging class"""
        self.chi2 = chi2
        self.ndof = ndof
        self.err = err
        if len(value_cols) != len(variance_cols):
            raise ValueError("Size mismatch between value and error columns.")
        self.value_cols = value_cols
        self.variance_cols = variance_cols

    def __repr__(self):
        _str = f"Labels:\n"
        labels = [
            f"{label}:{getattr(self, label)}" for label in dir(self) if label[0] != "_"
        ]
        return _str + "\n".join(labels)
