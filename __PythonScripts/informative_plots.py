import matplotlib.pyplot as plt
from __PythonScripts.circularTransformations import *
from __PythonScripts.descriptiveStats import *
from __PythonScripts.read_data import *


def InformativePlots():
    # Creating big figure to hold all
    fig = plt.figure(figsize=(14, 8))

    # setting font size
    plt.rcParams.update({'font.size': 8})

    # estimated mu vs. response mu
    ax0 = fig.add_subplot(241)
    ax0.scatter(res_mu, est_mu, marker='.', label=f'n={len(res_mu)}')
    ax0.legend()
    ax0.set_title('\nParticipant response mu by estimated mu')
    ax0.set_xlabel('response mu (radians)')
    ax0.set_ylabel('estimated mu (radians)')
    ax0.set_xticks(card_direc)
    ax0.set_yticks(card_direc)

    # Probe init vs. est_mu
    ax6 = fig.add_subplot(243)
    ax6.hist(probe2est, bins=40)
    ax6.set_title(' Initial Probe to Estimated Mu')
    ax6.set_ylabel('Count')
    ax6.set_xlabel('Distance initial probe (degrees)')

    # Probe init vs. res_mu
    ax7 = fig.add_subplot(242)
    ax7.hist(probe2res, bins=40)
    ax7.set_title('Initial Probe to Response Mu')
    ax7.set_ylabel('Count')
    ax7.set_xlabel('Distance initial probe (degrees)')

    # # Est_mu vs. Err
    # ax1 = fig.add_subplot(245)
    # ax1.plot(np.unique(est_mu) * 360 / (2 * np.pi), avgMuErr_ResxEst, color='orange', linewidth=.5)
    # # ax1.scatter(np.unique(est_mu)*360/(2*np.pi), avgMuErr_ResxEst, color='orange',s=1, marker='.')
    # ax1.set_xlabel('Est_mu (degrees)')
    # ax1.set_ylabel('Mean Absolute Error (degrees)')
    # ax1.set_title('Mean Absolute Error across estimated mus')

    # PT vs. RT
    ax1 = fig.add_subplot(245)
    ax1.set_xlabel('presentation time (ms)')
    ax1.set_ylabel('response time (ms)')
    ax1.set_title('PT vs. RT')
    ax1.set_xticks(np.arange(8))
    ax1.set_xticklabels(durVal.astype(int))
    ax1.plot(np.arange(9), RTxPT)

    # Error vs. PT
    ax2 = fig.add_subplot(246)
    ax2.set_title('Error vs. PT')
    ax2.set_xlabel('Presentation Time (ms)')
    ax2.set_ylabel('Mean Absolute Error (degrees)')
    ax2.set_xticks(np.arange(9))
    ax2.set_xticklabels(durVal.astype(int))
    ax2.plot(np.arange(len(durVal)), ERxPT)

    # Error vs. RT
    ax8 = fig.add_subplot(244)
    ax8.plot(uniqRT, avgRTxEr)
    ax8.set_title('RT vs. Error')
    ax8.set_xlabel('Response time (ms)')
    ax8.set_ylabel('Absolute Error (degrees)')

    # Binned Error vs.RT
    ax8 = fig.add_subplot(247)
    ax8.scatter(uniqRTbinned, avgRTxERbinned)  # plotting scatter, each point avg'd over equal number of RTs
    ax8.set_title('Binned RT vs. Error')
    ax8.set_xlabel(f'Binned Response time (ms)\n {bins} bins, bin size = {fs[-1]}')
    ax8.set_ylabel('Absolute Error (degrees)')

    # plotting RT distribution
    ax5 = fig.add_subplot(248)
    ax5.hist(keyRT, bins=180, color='cornflowerblue')
    ax5.spines['right'].set_visible(False)
    ax5.spines['top'].set_visible(False)
    ax5.set_title('Response Time \n(all trials)')
    ax5.set_ylabel('Count')
    ax5.set_xlabel('Response Time (ms)')

    fig.tight_layout()
