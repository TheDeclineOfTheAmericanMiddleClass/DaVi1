import scipy.stats
from __PythonScripts.read_data import *
from __PythonScripts.circularTransformations import *

# Error between theoretical parameters and estimated parameters from distributions drawn in trials
avgMuErr_SimxEst = abs_err(sim_mu, est_mu).mean()
estKappa_err = abs_err(sim_kappa, est_kappa).mean()  # kappa estimated with MLE

avgERxTrials = ERxTrials.mean()  # average participant error across trails
avgERxCard = ERxTrials[cardinalTrials].mean()  # average error in cardinal directions
avgRTxCard = keyRT[cardinalTrials].mean()  # average response time in cardinal directions
avgERxObli = ERxTrials[obliqueTrials].mean()  # average error in oblique directions
avgRTxObli = keyRT[obliqueTrials].mean()  # average response time in oblique directions

# # MAE for non cardinal, non oblique directions, using mask
# non_OC = np.ones_like(est_mu, dtype=bool)  # creating boolean mask
# non_OC[cardinalTrials] = 0
# non_OC[obliqueTrials] = 0
# nonOC_Err = abs_err(est_mu[non_OC], res_mu[non_OC]).mean()

# calculating error -- total, by presentation time, and SNR
ERxPT = np.ones(len(durVal))  # MAE, by visualization durations
SEMxPT = np.ones(len(durVal))  # SEM, by visualization durations
for i, x in enumerate(durVal):
    ERxPT[i] = abs_err(est_mu[durInd[x]], res_mu[durInd[x]]).mean()  # durInd is a dictionary
    SEMxPT[i] = scipy.stats.sem(abs_err(est_mu[durInd[x]], res_mu[durInd[x]]))

allsignedER = signed_err(est_mu, res_mu)  # single trial signed error
allER = abs_err(est_mu, res_mu)  # single trial absolute error
loER = abs_err(est_mu[loSNR], res_mu[loSNR])  # single trial errors x SNR
hiER = abs_err(est_mu[hiSNR], res_mu[hiSNR])

# single trial errors x SNR
signed_trialERxPT = [list(allsignedER[durInd[x]]) for i, x in enumerate(durVal)]

# Mean and standard deviation of RT, by visualization duration
avgRTxPT = np.ones([len(durInd)])
stdRTxPT = np.ones([len(durInd)])

for i, x in enumerate(durVal):
    avgRTxPT[i] = np.mean(keyRT[durInd[x]])
    stdRTxPT[i] = np.std(keyRT[durInd[x]])

# Calculating mean for each kappa-propmix combination
for i, x in enumerate(propVal):  # for each propmix value
    # TODO: ensure mean RT is being accurately calculated here
    _mean = []
    for key_ind, key in enumerate(kp_RT[i].keys()):  # for each kappa value
        _mean.append(np.mean(kp_RT[i][key]))
    # Mean RT values, kappa values for each propmix
    kp_RT_mean.append(_mean)
    kpVal.append(list(kp_RT[i].keys()))

## Checking for order effects and est_mu orientation preference
# Average RT and Accuracy by trial # and est_mu values
# Output: trialRT_mean, trialAC_mean, muRT_mean, avgMuErr_ResxEst
trialRT_mean = []
trialAC_mean = []
muRT_mean = []
avgMuErr_ResxEst = []
dummy = 0.

for i, trinum in enumerate(np.unique(trial)):
    sing_tri = np.where(trial == trinum)[0]  # indices for specific trial
    trialRT_mean.append(np.mean(keyRT[sing_tri]))  # mean reaction time for specific trial
    trialAC_mean.append(np.mean(ERxTrials[sing_tri]))  # mean accuracy for specific trial

for i, muval in enumerate(np.unique(est_mu)):
    sing_mu = np.where(est_mu == muval)[0]  # indices for single mu value
    muRT_mean.append(np.mean(keyRT[sing_mu]))
    avgMuErr_ResxEst.append(np.mean(ERxTrials[sing_mu]))  # TODO: look into why there is decreased accuracy ~pi/2

signed_trialRTxPT = [list(keyRT[durInd[x]]) for i, x in enumerate(durVal)]
uniqRT = np.unique(keyRT)
avgRTxEr = np.empty_like(uniqRT)
for i, x in enumerate(uniqRT):
    avgRTxEr[i] = np.mean(ERxTrials[np.where(keyRT == uniqRT[i])])  # TODO: add list of error for every trial

# creating binned uniqRT and avgRTxEr
from functools import reduce


# factor-finding function, to facilitate even binning
def factors(n):
    return set(reduce(list.__add__,
                      ([i, n // i] for i in range(1, int(n ** 0.5) + 1) if n % i == 0)))


fs = [x for x in list(factors(len(uniqRT))) if x < 50]
fs.sort()
bins = int(len(uniqRT) / fs[-1])
avgRTxERbinned = np.mean(avgRTxEr.reshape(-1, bins), axis=1)
uniqRTbinned = np.mean(uniqRT.reshape(-1, bins), axis=1)