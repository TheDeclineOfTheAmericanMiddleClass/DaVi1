import scipy.stats as stats
from __PythonScripts.descriptiveStats import *
from __PythonScripts.nls_funcs import *

# setting variable for gamma histogram
RT_y = np.histogram(keyRT, bins=180)[0]  # NOTE: 180 bins hardcoded in nls_fit.py. Must be changed there as well
RT_x = np.mean((np.histogram(keyRT, bins=180)[1][:-1], np.histogram(keyRT, bins=180)[1][1:]), axis=0)  # bin center

# setting variables to pass to NLS_fit
losstypes = ['linear', 'soft_l1', 'huber', 'cauchy', 'arctan']
curvenames = ['exponential', 'four-parameter logistic', 'gamma']
empty = ['', '', '']
curvefuncs = [expfunc, fourfunc, gdfunc]
lossfuncs = [exp_lossfunc, four_lossfunc, gd_lossfunc]
data_x = [vizDur, vizDur, RT_x]
data_y = [ERxTrials, ERxTrials, RT_y]
gt = [ERxPT, ERxPT, keyRT]  # ground truth
bp = ['scatter', 'scatter', 'hist']  # baseplots
xlabels = ["presentation time (ms)", "presentation time (ms)", "reaction time (ms)"]
ylabels = ["error (abs. degrees)", "error (abs. degrees)", 'count']


# setting trial&error-chosen initial values
x0_exp = np.array([14.0, 1.0, 0.0])
x0_four = np.array([40.0, 3.0, 100, 15.0])
gdscal = RT_y.max() / stats.gamma.pdf(RT_x, 6, 0, 250).max()  # scaling to make gamma bigger
x0_gd = np.array([6, 250, gdscal])  # x = [shape k, scale theta, size]
x0 = [x0_exp, x0_four, x0_gd]

caption3 = f'Figure 3. 851 unique participant-initiated reaction times, as function of \nmean absolute error, ' \
           f'averaged into 23 bins, each of size 37.\nEach point is plotted at bin\'s mean. Range: 408 - 11692 ms.'

caption4 = f'Figure 4. Testing different loss functions and fit functions for non-linear least squares model.' \
           f'\nParameters were estimated for (a) an exponential function, (b) a four-parameter logistic,' \
           f'and \n(c) a gamma function. Experiment results in blue.'

caption5 = f'Figure 5. Experiment results in blue, stratified by signal-to-noise ratio.\nNon-linear least squares ' \
           f'model of the absolute degree of ' \
           f'participant error in estimating the mean, fit with \n(a) a four-parameter logistic function.' \
           f' (b) Model of the distribution ' \
           f'of all participant\'s reaction times, fit with a gamma distribution.' \
           f'\nEach model was best fit with a linear loss function. Error bars reflect standard error of the mean.'

# # setting bounds to avoid overflow runtime error
# bounds = [[(ERxPT.min(), 1e-4, -1e3), (ERxPT.max(), 1e1, 1e3)],  # bounds for exponential
#           [(ERxPT.max(), 0, 50, ERxPT.min()), (150, 5, np.inf, ERxPT.max())],  # bounds for 4 param
#           [-np.inf, np.inf]]
