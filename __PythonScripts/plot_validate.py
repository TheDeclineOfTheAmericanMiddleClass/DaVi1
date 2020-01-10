import matplotlib.pyplot as plt
from pilot_funcs import *
from pilot_stats import *
from read_data import *


def Plot_Validate():
    fig = plt.figure(figsize=(12, 4))
    # ax = fig.add_subplot(111)  # The big subplot
    #
    # # Turn off axis lines and ticks of the big subplot
    # ax.spines['top'].set_color('none')
    # ax.spines['bottom'].set_color('none')
    # ax.spines['left'].set_color('none')
    # ax.spines['right'].set_color('none')

    # #Plot title
    # plt.rcParams.update({'font.size': 11})
    # plt.suptitle('PLOTS FOR VALIDATION')

    # setting font size
    plt.rcParams.update({'font.size': 8})

    # Plotting estimated mu vs. response mu
    ax0 = fig.add_subplot(131)
    ax0.scatter(res_mu, est_mu, marker='.', label=f'n={len(res_mu)}')
    ax0.legend()
    ax0.set_title('\nParticipant response as a function of estimated mu')
    ax0.set_xlabel('response mu (radians)')
    ax0.set_ylabel('estimated mu (radians)')
    ax0.set_xticks(card_direc)
    ax0.set_yticks(card_direc)

    ax1 = fig.add_subplot(132)
    ax1.scatter(answer_x[card_ind], answer_y[card_ind], marker='.')
    ax1.set_xlabel('answer_x')
    ax1.set_ylabel('answer_y')
    ax1.set_title('Participant response\nest_mu in CARDINAL directions')

    ax2 = fig.add_subplot(133)
    ax2.scatter(answer_x[obli_ind], answer_y[obli_ind], marker='.')
    ax2.set_title('Participant response\nest_mu in OBLIQUE directions')
    ax2.set_xlabel('answer_x')
    ax2.set_ylabel('answer_y')

    fig.tight_layout()
