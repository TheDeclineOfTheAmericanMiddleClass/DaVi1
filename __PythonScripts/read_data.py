# ## Reading in data
import numpy as np
import glob
import os
from __PythonScripts.circularTransformations import *

# os.chdir('/media/locallab/Windows/Users/Public/Documents/DataViz/behav')
os.chdir(r'C:\Users\a\Documents\BCCN\Rolfs_Lab\DaVi1')
data_files = glob.glob('_datfiles/*.dat')  # only files starting w# ith 'd', no training files
data = np.genfromtxt(data_files[0]).T  # allocating

# Adding all participant files to one matrix for within subjects analysis
for i, file in enumerate(data_files):

    if i == 0:
        data = np.genfromtxt(file).T

    else:
        more_data = np.genfromtxt(file).T

        if more_data.shape[0] != 23:  # data.shape[0]:  # doesn't read in data with missing dimensions
            print(f'Data for {file} not being read due to dimensionality of {more_data.shape}\n')
            continue

        else:
            data = np.hstack((data, more_data))

assert data.shape[0] == 23, 'Data does not have 23 dimensions'

# Data dimension labels
colnames = ["block", "trial", "imageid", "testcond", "cueTim",
            "sim_mu", "sim_kappa", "propmix",
            "est_mu", "est_sd", "est_kappa",
            "probe_init_x", "probe_init_y", "linesize",
            "tFix", "tvizOn", "tvizOf",
            "tProbeOn", "tRes", "tclear",
            "answer_x", "answer_y", "keyRT"]  # TODO: ensure probe_init_y is actually that, typo from Sven

## Attempting easy reference of variable names by their string values
## Using setattr to create data class with variables from strings
# class data:
#     def __init__(self, colnames):
#         for i,x in enumerate(colnames):
#             name = x
#             value = data[colnames.index(x)]
#             setattr(self, name, value)
#
# for i, x in enumerate(colnames):
#     exec(f"%s = %a" % (x, data[colnames.index(x)]))
#     np.set_printoptions(threshold=np.inf)
#     exec(f"{x} = np.array({data[colnames.index(x)]})")

# # Creating dictionary of data values for easy reference
# data_dict = dict(zip(colnames, zip(data)))


## Defining experiment parameters and response values
# Note: tFix always 0.0, tvizOn always 500.0, tclear always ~216.0 (blank screen time after response)
time_data = data[14:20]
tvizOf = data[colnames.index('tvizOf')]
tvizOn = data[colnames.index('tvizOn')]
tclear = data[colnames.index('tclear')]  # time to reset experiment loop
tRes = data[colnames.index('tRes')]
sim_mu = data[colnames.index('sim_mu')]
sim_kappa = data[colnames.index('sim_kappa')]
est_mu = data[colnames.index('est_mu')]
est_kappa = data[colnames.index('est_kappa')]
keyRT = data[colnames.index('keyRT')]
propmix = data[colnames.index('propmix')]
block = data[colnames.index('block')]
trial = data[colnames.index('trial')]

# transforming x and y values to customary cartesian plane values
probe_init_y = data[colnames.index('probe_init_y')] * -1.
probe_init_x = data[colnames.index('probe_init_x')] * -1.
answer_x = data[colnames.index('answer_x')] * -1.
answer_y = data[colnames.index('answer_y')] * -1.

vizDur = tvizOf - tvizOn  # visualization duration

# Specifying cardinal vs. oblique
card_pad = obli_pad = np.pi / 16  # Padding when analyzing directions
card_direc = [0, np.pi / 2, np.pi, 3 * np.pi / 2, np.pi * 2]  # cardinal directions
obli_direc = [np.pi / 4, 3 * np.pi / 4, 5 * np.pi / 4, 7 * np.pi / 4]  # oblique directions

cardinalTrials = circ_window(card_direc, est_mu, pad=card_pad)  # trials with mu in cardinal directions (padded)
obliqueTrials = circ_window(obli_direc, est_mu, pad=obli_pad)  # trials with mu in oblique directions (padded)
otherTrials = np.array(list(set(np.arange(len(est_mu))) - set(cardinalTrials) - set(obliqueTrials)))

# nominal array of directions
directions = np.arange(len(est_mu))
directions[otherTrials] = 0  # 'other'
directions[cardinalTrials] = 1  # 'cardinal'
directions[obliqueTrials] = 2  # 'oblique'

# Calculating differences between response, estimated, and initial probe mu
_, res_mu = cart2pol(answer_x, answer_y)  # participants' responses for mu, in radians
_, init_mu = cart2pol(probe_init_x, probe_init_y)  # randomly initialized mu of response probe

probe2est = abs_err(est_mu, init_mu)  # degree difference between probe and estimated
probe2res = abs_err(res_mu, init_mu)  # degree difference between probe and response
ERxTrials = abs_err(res_mu, est_mu)  # degree difference between estimated and response

avgRTxCard = keyRT[cardinalTrials].mean()  # mean RT for cardinal directions
avgRTxObli = keyRT[obliqueTrials].mean()  # mean RT for oblique directions

## Specifying trial numbers for each possible presentation duration, kappa value, and propmix
durInd = {}  # the dictionary
durVal = np.unique(vizDur)
dur_RT = []
RTxPT = np.zeros_like(durVal)
for i, x in enumerate(durVal):
    durInd[x] = np.where(vizDur == x)  # adding entries for each duration to the dictionary
    dur_RT.append(keyRT[durInd[x]])  # adding list of reaction times to a list
    RTxPT[i] = np.mean(dur_RT[i])

kapInd = {}
kapVal = np.unique(est_kappa)
kap_RT = []
kap_RT_mean = []
for i, x in enumerate(kapVal):
    kapInd[x] = np.where(est_kappa == x)
    kap_RT.append(keyRT[kapInd[x]])
    kap_RT_mean.append(np.mean(kap_RT[i]))

propInd = {}
propVal = np.unique(propmix)
prop_RT = []
prop_RT_mean = []
for i, x in enumerate(propVal):
    propInd[x] = np.where(propmix == x)
    prop_RT.append(keyRT[propInd[x]])
    prop_RT_mean.append(np.mean(prop_RT[i]))

allInd = np.arange(len(est_mu))
hiSNR = propInd[0.5][0].astype(int)
loSNR = propInd[0.0][0].astype(int)
bothSNR = [loSNR, hiSNR]

# Specifying the reaction time for each combination of kappa and propmix
# kp_RT = {}  # dictionary of dictionaries, one for each propmix value
kp_RT = []  # alternate implementation
kp_RT_mean = []
kpVal = []
for i, x in enumerate(propVal):  # for each propmix value
    kap_by_propVal = {}
    for j, y in enumerate(kapVal):
        for k, z in enumerate(keyRT):
            if est_kappa[k] == y and propmix[k] == x:
                # TODO: ensure kap_by_propVal keys are calculated correctly in above if statement
                kap_by_propVal.setdefault(y, []).append(z)  # create list for each kappa
    # kp_RT[x] = kap_by_propVal  # appending dictionary of each propmix's kappas to a dictionary
    kp_RT.append(kap_by_propVal)  # alternate implementation

# Reading in demogrpahic data
import pandas as pd

demos = pd.read_excel('RolfsLab_ParticipantsInfo.xlsx')
ex_code = demos.keys()[2]
age = demos.keys()[3]
gender = demos.keys()[4]
dom_eye = demos.keys()[5]
dom_hand = demos.keys()[6]
demos = demos.loc[(demos[ex_code] == 'DAVI1')]  # filtering for Davi1 participants

left_h = (demos.loc[:, dom_hand] == np.unique(demos.loc[:, dom_hand])[0]).sum()
left_e = (demos.loc[:, dom_eye] == np.unique(demos.loc[:, dom_eye])[0]).sum()
wom = (demos.loc[:, gender] == np.unique(demos.loc[:, gender])[0]).sum()
min_age = demos.loc[:, age].min()
max_age = demos.loc[:, age].max()

print(f'Out of {len(demos)} participants, there were... \n'
      f'Left-handed:{left_h}, Right-handed = {len(demos) - left_h}\n'
      f'Left eye dominant:{left_e}, Right eye dominant: {len(demos) - left_e}\n'
      f'Min age: {min_age}, Max age: {max_age}\n'
      f'Women: {wom}, Men: {len(demos) - wom}')
