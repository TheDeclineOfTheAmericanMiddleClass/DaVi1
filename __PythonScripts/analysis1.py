from __PythonScripts.informative_plots import *
from __PythonScripts.nls_fit import *
from __PythonScripts.fit_var import *

# This script is for analysis of pilot data for the Circular Data Visualization Project
# Team Members: Adu Matory, Sven Ohl, Bryce Yahn, Martin Rolfs, Jan Klanke, Tobi
# Last Updated: Dec 5, 2019

# Printing basic descriptive statistics
summary_stats()

# # Validating data/plotting what's informative
# InformativePlots()

# Fitting curve!
residuals = NLSfit(data_x, data_y, x0, curvenames, curvefuncs, losstypes, lossfuncs, gt,
                   xlabels, ylabels, errorbs, baseplot=bp)

# fitting gamma distribution with MLE
import scipy.stats as stats
# # fixing x > 0 problem by only using > 0 values of RT_y
# locloc = np.where(RT_y > 0)[0]
# fit_alpha, fit_loc, fit_beta = stats.gamma.fit(RT_y[locloc], floc=0)
# plop = stats.gamma.pdf(RT_x[locloc], fit_alpha, fit_loc, fit_beta)
# # adding 1 to attempt to solve problem
# fit_alpha, fit_loc, fit_beta = stats.gamma.fit(RT_y+1)
# plop = stats.gamma.pdf(RT_x, fit_alpha, fit_loc, fit_beta)
