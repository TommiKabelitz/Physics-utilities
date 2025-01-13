def plot_settings(mpl):
    mpl.rcParams["ytick.labelsize"] = 16
    mpl.rcParams["xtick.labelsize"] = 16
    mpl.rcParams["xtick.direction"] = "inout"
    mpl.rcParams["ytick.direction"] = "inout"
    pres_params = {"font.size": 22, "legend.fontsize": 16, "legend.numpoints": 1}
    pres_params["figure.autolayout"] = True
    mpl.rcParams.update(pres_params)
    mpl.rcParams["errorbar.capsize"] = 3  # restoring the caps on error bars
    mpl.rcParams["lines.markeredgewidth"] = 0.5
    mpl.rcParams["figure.max_open_warning"] = 10
    DerekSettings = {
        "font.serif": ["Computer Modern"],
        "font.size": 18,
        "lines.markersize": 6.0,
    }
    mpl.rcParams.update(DerekSettings)