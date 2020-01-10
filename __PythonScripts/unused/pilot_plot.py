import matplotlib.pyplot as plt
from pilot_funcs import *
from stats_pilot import *
from read_data import *


## Plotting estimated mu vs. participant response

def Pilot_Plot():
    # Creating big figure to hold all
    fig = plt.figure(figsize=(20, 16))

    # setting font size
    plt.rcParams.update({'font.size': 8})

    # # Turn off axis lines and ticks of the big subplot
    # ax.spines['top'].set_color('none')
    # ax.spines['bottom'].set_color('none')
    # ax.spines['left'].set_color('none')
    # ax.spines['right'].set_color('none')

    # Plotting estimated mu vs. response mu
    ax0 = fig.add_subplot(231)
    ax0.scatter(res_mu, est_mu, marker='.', label=f'n={len(res_mu)}')
    ax0.legend()
    ax0.set_title('FOR VALIDATION: Participant response as a function of estimated mu')
    ax0.set_xlabel('response mu (radians)')
    ax0.set_ylabel('estimated mu (radians)')
    plt.set_xticks(card_direc)
    plt.set_yticks(card_direc)

    # Plotting MSE across presentation times
    ax1 = fig.add_subplot(232)
    ax1.set_title('MSE across stimulus presentation times')
    ax1.set_xlabel('Presentation Times (ms)')
    ax1.set_ylabel('MSE')
    # plt.bar(np.arange(8), durMSE, width=0.2)
    ax1.plot(np.arange(8), durMSE)
    ax1.set_xticks(np.arange(8), labels=durVal)

    #######################################################################################################
    # # Plotting response time vs. estimated mu, vs. response_mu
    # plt.figure(figsize=(13,6))
    #
    # plt.subplot(211)
    # plt.scatter(est_mu, data[colnames.index('keyRT')], marker='.', label=f'n={len(est_mu)}')
    # plt.legend()
    # plt.title('Response time as a function of estimated mean location')
    # plt.xlabel('est_mu (radians)')
    # plt.ylabel('response time (ms)')
    #
    # plt.subplot(212)
    # plt.scatter(res_mu, data[colnames.index('keyRT')], marker='.',label=f'n={len(res_mu)}')
    # plt.legend()
    # plt.title('Response time as a function of participant-observed mean location')
    # plt.xlabel('response mu (radians)')
    # plt.ylabel('response time (ms)')
    #
    # plt.tight_layout()
    # plt.show()

    # #######################################################################################################
    # ## Plotting cardinal vs. oblique MSE
    # plt.figure(figsize=(4,3))
    # plt.title('MSE, by orientation of MSE \n(each direction padded by pi/8 radians')
    # plt.bar([0, 1], [card_MSE, obli_MSE])
    # plt.ylabel('MSE')
    # plt.xticks([0,1], ('cardinal','oblique'))
    # plt.show()

    #######################################################################################################
    ## Plotting relationship of accuracy with RT and PT
    ## TODO: Plot SAT curve after fitting logistic function
    plt.figure(figsize=(14, 4))
    plt.rcParams.update({'font.size': 6})

    ax2 = fig.add_subplot(233)
    # plt.title('Response time-Accuracy')
    # plt.xlabel('Response time (ms)')
    # plt.ylabel('Accuracy (percent distance of response mu from est_mu)')
    # plt.scatter(keyRT, ERxTrials * 100, marker='.', s=1)
    # plt.xticks(durVal, labels=durVal)

    ax2.set_title('Presentation Time vs. Accuracy')
    ax2.set_xlabel('Presentation time (ms)')
    ax2.set_ylabel('Accuracy (percent distance of response mu from est_mu)')
    ax2.scatter(vizDur, res_acc * 100)
    ax2.set_xticks(durVal, labels=durVal)

    # Boxplot, Response time median, mean, IQR for each stimulus duration
    ax3 = fig.add_subplot(234)
    ax3.set_title('Response time, by stimulus duration \n(orange = median, green = mean)')
    ax3.set_ylabel('Response time (ms)')
    ax3.set_xlabel('Presentation duration (ms)')
    ax3.boxplot(dur_RT, meanline=True, showmeans=True)
    ax3.set_xticks(np.arange(1, len(durVal) + 1), labels=durVal)

    #######################################################################################################
    # ## Accuracy as a function of distance of initial probe to (1) response mu and (2) estimated mu
    # fig = plt.figure(figsize=(10,5))
    #
    # ax = fig.add_subplot(111)  # The big subplot
    # ax1 = fig.add_subplot(211)
    # ax2 = fig.add_subplot(212)
    #
    # # Turn off axis lines and ticks of the big subplot
    # ax.spines['top'].set_color('none')
    # ax.spines['bottom'].set_color('none')
    # ax.spines['left'].set_color('none')
    # ax.spines['right'].set_color('none')
    # ax.tick_params(labelcolor='w', top='off', bottom='off', left='off', right='off')
    # ax.set_ylabel('Trial Accuracy')
    #
    # # fig.suptitle('Accuracy vs. probe locations')
    # ax1.scatter(probe2est, ERxTrials, marker='.', s=1)
    # ax1.set_xlabel('distance from initial probe to estimated mu (radians)')
    # ax2.scatter(probe2res, ERxTrials, marker='.', s=1)
    # ax2.set_xlabel('distance from initial probe to response mu (radians)')
    # plt.tight_layout()
    #
    # plt.figure(figsize=(14, 4))
    # plt.rcParams.update({'font.size': 6})

    ax4 = fig.add_subplot(235)
    plt.title('Presentation Time-Accuracy Curve')
    plt.xlabel('Presentation time (ms)')
    plt.ylabel('Accuracy (percent distance of response mu from est_mu)')
    plt.scatter(vizDur, res_acc * 100)
    plt.xticks(durVal, labels=durVal)

    plt.title('Error vs. Propmix')
    plt.xlabel('Response time (ms)')
    plt.ylabel('Accuracy (percent distance of response mu from est_mu)')
    plt.scatter(keyRT, res_acc * 100, marker='.', s=1)
    # plt.xticks(durVal, labels=durVal)

    plt.figure(figsize=(12, 4))
    plt.rcParams.update({'font.size': 12})
    plt.suptitle('Parameter dependency on response time')
    plt.rcParams.update({'font.size': 8})
    plt.subplot(121)
    plt.title('Mean response time as a function of kappa (concentration) of stimulus')
    for i, x in enumerate(propVal):
        plt.plot(kpVal[i], kp_RT_mean[i], label=f'propmix = {x}')
    plt.legend()
    plt.xlabel('estimated kappa')
    plt.ylabel('mean RT (ms)')
    plt.title('RT by kappa')

    ## All kappa
    # plt.plot(kapVal, kap_RT_mean)
    # plt.xlabel('kappa')
    # plt.ylabel('mean RT (ms)')

    plt.subplot(122)
    plt.bar(propVal, prop_RT_mean)
    plt.title('Mean response time as a function of noise present')
    plt.xlabel('Proportion of uniform noise to von Mises distribution in stimulus')
    plt.ylabel('mean RT (ms)')
    plt.xticks(propVal)

    # TODO: plot kappa/propmix as function of error
