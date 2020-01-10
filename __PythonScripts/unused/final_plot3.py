import matplotlib.pyplot as plt
from __PythonScripts.circularTransformations import *
from pilot_stats import *
from read_data import *


## Plotting estimated mu vs. participant response
def Final_Plot3():
    fig = plt.figure(figsize=(9, 5))

    # ax9 = fig.add_subplot(224)
    # ax9.plot(np.unique(est_mu), muRT_mean, color='blue', linewidth=1)
    # ax9.set_xlabel('est_mu (radians)')
    # ax9.set_ylabel('mean response time(ms)')
    # ax9.set_title('WHY DOES THIS DIP?\nMean response time per est_mu')

    ax8 = fig.add_subplot(222)
    ax8.plot(np.unique(est_mu), avgMuErr_ResxEst, color='orange', linewidth=1)
    ax8.set_xlabel('est_mu (radians)')
    ax8.set_ylabel('WHY DOES THIS DIP?\n mean trial accuracy (radians)')
    ax8.set_title('Mean accuracy per est_mu')

    ax1 = fig.add_subplot(223)
    ax1.set_title('WHY ISN''T THIS MONOTONICALLY INCREASING \nError across stimulus presentation times')
    ax1.set_xlabel('Presentation Times (ms)')
    ax1.set_ylabel('Mean Angular Error (%)')
    ax1.set_xticks(np.arange(8))
    ax1.set_xticklabels(durVal.astype(int))
    ax1.plot(np.arange(len(durVal)), ERxPT)

    ## Plotting relationship of accuracy with RT and PT (presentation time)
    avg_ra = np.empty_like(np.unique(vizDur))
    uni_VD = np.unique(vizDur)
    for i, x in enumerate(uni_VD):
        print(i)
        avg_ra[i - 1] = np.mean(ERxTrials[np.where(vizDur == uni_VD[i - 1])])

    ax2 = fig.add_subplot(221)
    ax2.set_title('Presentation duration vs. Accuracy')
    ax2.set_xlabel('Presentation duration (ms)')
    ax2.set_ylabel('Angular Accuracy (%)')
    ax2.plot(uni_VD, avg_ra, marker='.')

    plt.tight_layout()
