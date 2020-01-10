import numpy as np
import matplotlib.pyplot as plt

# from sklearn import metrics

# reading in, reshaping, removing NaNs from data
pRatio = np.genfromtxt(
    '/media/locallab/Windows/Users/Public/Documents/DataViz/behav/_MLEdata/performanceRatio10.10.19.txt')
pRatio = np.reshape(pRatio, (7, int(pRatio.size / 7)))

optAlg = ["NR", "BFGS", "BFGSR", "SANN", "CG", "NM"]
tau = np.arange(min(pRatio[~np.isnan(pRatio)]), max(pRatio[~np.isnan(pRatio)]) / 4, .25)

## Allocating performance profile
pProfile = np.empty((len(optAlg), len(tau)))

for j, alg in enumerate(optAlg):
    for i, tVal in enumerate(tau):
        pProfile[j, i] = np.sum([pRatio[j] < tVal]) * (7 / pRatio.size)

fig = plt.figure(figsize=(7, 7 / 1.618))
plt.suptitle('Performance profile of MLE Optimization Algorithms')
leg_size = 9

ax0 = fig.add_subplot(121)
for i, x in enumerate(optAlg):
    ax0.plot(tau, pProfile[i], marker='.', markersize=4, linewidth='1.2', label=f'{optAlg[i]}', )
ax0.legend(prop={'size': leg_size}, loc=4)
ax0.set_xlabel(r'$\tau$')
ax0.set_ylabel(r'$\rho_s(\tau)$')

ax1 = fig.add_subplot(122)
for i, x in enumerate(optAlg):
    # fpr, tpr, thresholds = metrics.roc_curve(np.log2(tau), pProfile[i], pos_label=2)
    ax1.plot(np.log2(tau), pProfile[i], marker='.', markersize=4, linewidth='1.2',
             label=f'{optAlg[i]}')  # , AUC:{metrics.auc(fpr, tpr)}')
ax1.legend(prop={'size': leg_size}, loc=4)
ax1.set_xlabel(r'$\log_2(\tau)$')
ax1.set_ylabel(r'$\rho_s(\tau)$')

fig.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()
