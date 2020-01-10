import scipy.stats as stats
from __PythonScripts.descriptiveStats import *
from __PythonScripts.nls_funcs import *

# setting variable for gamma histogram
RT_y = np.histogram(keyRT, bins=180)[0]  # NOTE: 180 bins hardcoded in nls_fit.py. Must be changed there as well
RT_x = np.mean((np.histogram(keyRT, bins=180)[1][:-1], np.histogram(keyRT, bins=180)[1][1:]), axis=0)  # bin center

# setting variables to pass to NLS_fit
losstypes = ['linear']  # , 'soft_l1', 'huber', 'cauchy', 'arctan']
curvenames = ['exponential', 'four-parameter logistic', 'gamma']
curvefuncs = [expfunc, fourfunc, gdfunc]
lossfuncs = [exp_lossfunc, four_lossfunc, gd_lossfunc]
data_x = [vizDur, vizDur, RT_x]
data_y = [ERxTrials, ERxTrials, RT_y]
gt = [ERxPT, ERxPT, keyRT]  # ground truth
bp = ['scatter', 'scatter', 'hist']  # baseplots
xlabels = ["presentation time (ms)", "presentation time (ms)", "reaction time (ms)"]
ylabels = ["error (abs. degrees)", "error (abs. degrees)", 'count']
errorbs = [STDxPT, STDxPT, []]

# setting trial&error-chosen initial values
x0_exp = np.array([14.0, 1.0, 0.0])
x0_four = np.array([40.0, 3.0, 100, 15.0])
gdscal = RT_y.max() / stats.gamma.pdf(RT_x, 6, 0, 250).max()  # scaling to make gamma bigger
x0_gd = np.array([6, 250, gdscal])  # x = [shape k, scale theta, size]
x0 = [x0_exp, x0_four, x0_gd]

# # setting bounds to avoid overflow runtime error
# bounds = [[(ERxPT.min(), 1e-4, -1e3), (ERxPT.max(), 1e1, 1e3)],  # bounds for exponential
#           [(ERxPT.max(), 0, 50, ERxPT.min()), (150, 5, np.inf, ERxPT.max())],  # bounds for 4 param
#           [-np.inf, np.inf]]
