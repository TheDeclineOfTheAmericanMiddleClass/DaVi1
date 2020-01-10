import matplotlib.pyplot as plt
from pilot_funcs import *
from pilot_stats import *
from read_data import *


## Plotting estimated mu vs. participant response
def Pilot_Plot2():
    # Creating big figure to hold all
    fig = plt.figure(figsize=(14, 8))
    # plt.rcParams.update({'font.size': 12})
    # plt.suptitle('?Parameter dependency on response time')

    # setting font size
    plt.rcParams.update({'font.size': 8})

    # Plotting estimated mu vs. response mu
    ax0 = fig.add_subplot(231)
    ax0.scatter(res_mu, est_mu, marker='.', label=f'n={len(res_mu)}')
    ax0.legend()
    ax0.set_title('FOR VALIDATION:\nParticipant response as a function of estimated mu')
    ax0.set_xlabel('response mu (radians)')
    ax0.set_ylabel('estimated mu (radians)')
    ax0.set_xticks(card_direc)
    ax0.set_yticks(card_direc)

    # Plotting error across presentation times
    ax1 = fig.add_subplot(235)
    ax1.set_title('Error across stimulus presentation times')
    ax1.set_xlabel('Presentation Times (ms)')
    ax1.set_ylabel('Mean Angular Error (%)')
    ax1.set_xticks(np.arange(8))
    ax1.set_xticklabels(durVal.astype(int))
    ax1.plot(np.arange(len(durVal)), durErr)

    ## Plotting relationship of accuracy with RT and PT (presentation time)
    ax2 = fig.add_subplot(236)
    ax2.set_title('Presentation duration vs. Accuracy')
    ax2.set_xlabel('Presentation duration (ms)')
    ax2.set_ylabel('Angular Accuracy (%)')
    ax2.scatter(vizDur, res_acc, marker='.')
    # ax2.set_xticks(durVal) # looks messy with ticks on in small graph
    # ax2.set_xlabels=(durVal)

    # ax2.set_title('Response time-Accuracy')
    # ax2.set_xlabel('Response time (ms)')
    # ax2.set_ylabel('Accuracy (percent distance of response mu from est_mu)')
    # ax2.scatter(keyRT, ERxTrials * 100, marker='.', s=1)
    # ax2.set_xticks(durVal, labels=durVal)

    # # Boxplot, Response time median, mean, IQR for each stimulus duration
    # ax3 = fig.add_subplot(234)
    # ax3.set_title('Response time, by stimulus duration \n(orange = median, green = mean)')
    # ax3.set_ylabel('Response time (ms)')
    # ax3.set_xlabel('Presentation duration (ms)')
    # ax3.boxplot(dur_RT, meanline=True, showmeans=True)
    # ax3.set_xticks(np.arange(1, len(durVal) + 1))
    # ax3.set_xticklabels(durVal.astype(int))

    # RT vs. accuracy
    ax4 = fig.add_subplot(232)
    ax4.set_title('Accuracy vs. RT')
    ax4.set_ylabel('Response time (ms)')
    ax4.set_xlabel('Angular accuracy (% max distance from mu)')
    ax4.scatter(res_acc, keyRT, marker='.', s=1)
    # ax4.xticks(durVal)
    # ax4.xlabels(durVal)

    # # RT vs. estimated variance (kappa)
    # ax5 = fig.add_subplot(236)
    # ax5.set_title('Mean response time as a function of kappa (concentration) of stimulus')
    # for i, x in enumerate(propVal):
    #     ax5.plot(kpVal[i], kp_RT_mean[i], label=f'propmix = {x}')
    #     # ax5.bar(np.mean(kpVal[i]), prop_RT_mean[i], color='black',width=.3)
    # ax5.legend()
    # ax5.set_xlabel('estimated kappa')
    # ax5.set_ylabel('mean RT (ms)')
    # ax5.set_title('RT by kappa')

    # # RT vs. estimated variance (kappa)
    # ax5 = fig.add_subplot(233)
    # ax5.set_title('Mean response time as a function of kappa (concentration) of stimulus')
    # for i, x in enumerate(propVal):
    #     if i == 0:
    #         kp_range = np.arange(np.min(np.min(kpVal)), np.max(np.max(kpVal)), .001)
    #         ax5.plot(kp_range, np.zeros_like(kp_range), color='black', label='mean')
    #     ax5.plot(kpVal[i], kp_RT_mean[i] - prop_RT_mean[i], label=f'propmix = {x}', alpha=.9)  # centered around mean
    # ax5.legend()
    # ax5.set_xlabel('estimated kappa')
    # ax5.set_ylabel('mean RT (ms), centered around mean')
    # ax5.set_title('RT by kappa')

    fig.tight_layout()

    fig2 = plt.figure(figsize=(9, 5))

    # hypothesis: null or sliiiight improvement
    ax6 = fig2.add_subplot(221)
    x = np.unique(trial)
    y = trialAC_mean
    fit = np.polyfit(np.unique(trial), (trialAC_mean), 1)
    fit_fn = np.poly1d(fit)
    ax6.plot(x, y, 'y-')
    ax6.plot(x, fit_fn(x), '--k', label=f'slope: {fit_fn[1]:.3}')
    ax6.legend()
    # ax6.plot(np.unique(trial), trialAC_mean, color='orange', linewidth=1)
    ax6.set_xlabel('trial number')
    ax6.set_ylabel('mean trial accuracy\n(radians, res_mu - est_mu)')
    ax6.set_title('Mean accuracy per trial')
    # TODO: fix ang_diff function, add radian-valued tick marks to y-axus

    # hypothesis: lower RT with higher trial, people want to hurry finishing
    ax7 = fig2.add_subplot(223)
    # ax7.plot(np.unique(trial), trialRT_mean, color='green', linewidth=1)
    x = np.unique(trial)
    y = trialRT_mean
    fit = np.polyfit(x, y, 1)
    fit_fn = np.poly1d(fit)
    ax7.plot(x, y, 'g-')
    ax7.plot(x, fit_fn(x), '--k', label=f'slope: {fit_fn[1]:.3}')
    ax7.legend()
    ax7.set_xlabel('trial number')
    ax7.set_ylabel('mean response time (ms)')
    ax7.set_title('Mean response time per trial')

    # hypothesis: bumps around oblique and/or cardinal directions
    ax8 = fig2.add_subplot(222)
    ax8.plot(np.unique(est_mu), muAC_mean, color='orange', linewidth=1)
    ax8.set_xlabel('est_mu (radians)')
    ax8.set_ylabel('mean trial accuracy\n(radians)')
    ax8.set_title('Mean accuracy per est_mu')
    # TODO: add ticks for cardinal and obliques

    # hypothesis: none
    ax9 = fig2.add_subplot(224)
    ax9.plot(np.unique(est_mu), muRT_mean, color='blue', linewidth=1)
    ax9.set_xlabel('est_mu (radians)')
    ax9.set_ylabel('mean response time(ms)')
    ax9.set_title('Mean response time per est_mu')

    fig2.tight_layout()

    # plotting reaciton time distribution
    fig, ax = plt.subplots()
    ax.hist(keyRT, bins=180, color='cornflowerblue')
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_title('Response Time \n(all trials)')
    ax.set_ylabel('Count')
    ax.set_xlabel('Response Time (ms)')
