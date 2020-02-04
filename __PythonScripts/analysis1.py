from __PythonScripts.informative_plots import *
from __PythonScripts.nls_fit import *
from __PythonScripts.fit_var import *

# This script is for analysis of pilot data for the Circular Data Visualization Project
# Team Members: Adu Matory, Sven Ohl, Bryce Yahn, Martin Rolfs, Jan Klanke, Tobi
# Last Updated: Dec 5, 2019

# Printing basic descriptive statistics
summary_stats()

# Validating data/plotting what's informative
InformativePlots()

# Fig 3. Binned Error vs.RT
fig = plt.figure(figsize=(7, 5))
fig.subplots_adjust(bottom=.2, top=.9)
plt.rcParams.update({'font.size': 8})
ax8 = fig.add_subplot(111)
ax8.scatter(uniqRTbinned, avgRTxERbinned)  # plotting scatter, each point avg'd over equal number of RTs
ax8.set_title('Binned RT vs. Error')
ax8.set_xlabel(f'Binned Response time (ms)')  # \n {bins} bins, bin size = {fs[-1]}')
ax8.set_ylabel('Absolute Error (degrees)')
plt.figtext(0.5, 0.01, caption3, wrap=True, ha='center', va='bottom', fontsize=8, fontstyle='italic')
fig.show()

# Fig 4. Fitting test curves!
test_cost, test_residuals = NLSfit(data_x, data_y, x0, cn=empty, cf=curvefuncs, ln=losstypes, lf=lossfuncs,
                                   groundtruth=gt, xlabels=xlabels, ylabels=ylabels, errorbar=False, caption=caption4,
                                   SNR=[allInd], baseplot=bp)

# Fig 5. Fitting best fit curves!
best_cost, best_residuals = NLSfit(datax=[vizDur, RT_x],
                                   datay=[ERxTrials, RT_y],
                                   fit_x0=[x0_four, x0_gd],
                                   cn=empty,
                                   cf=[fourfunc, gdfunc],
                                   ln=['linear'],
                                   lf=[four_lossfunc, gd_lossfunc],
                                   groundtruth=[ERxPT, keyRT],
                                   xlabels=xlabels[1:], ylabels=ylabels[1:],
                                   errorbar=True,
                                   caption=caption5,
                                   SNR=[loSNR, hiSNR],
                                   SNRstr=['low SNR', 'high SNR'],
                                   baseplot=['scatter', 'hist'],
                                   test=False)



# fitting gamma distribution with MLE
import scipy.stats as stats
# # fixing x > 0 problem by only using > 0 values of RT_y
# locloc = np.where(RT_y > 0)[0]
# fit_alpha, fit_loc, fit_beta = stats.gamma.fit(RT_y[locloc], floc=0)
# plop = stats.gamma.pdf(RT_x[locloc], fit_alpha, fit_loc, fit_beta)
# # adding 1 to attempt to solve problem
# fit_alpha, fit_loc, fit_beta = stats.gamma.fit(RT_y+1)
# plop = stats.gamma.pdf(RT_x, fit_alpha, fit_loc, fit_beta)
