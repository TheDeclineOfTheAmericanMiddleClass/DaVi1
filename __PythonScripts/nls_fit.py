from scipy.optimize import least_squares
import matplotlib.pyplot as plt
from __PythonScripts.read_data import *
from __PythonScripts.pilot_stats import allER
import scipy.stats


# Testing different lossnames and plotting various curve functions in loop
def NLSfit(datax, datay, fit_x0, cn, cf, ln, lf, groundtruth, xlabels, ylabels, caption, errorbar, SNR=allInd,
           SNRstr='', baseplot='scatter', test=True):
    """Takes arrays of each of the following: type of loss, curve function to fit, name of curve function,
    initial conditions for each type of curve, groundtruth, x-axis and y-axis labels, every signal to noise ratio"""

    # setting up figure
    fig, axs = plt.subplots(1, len(cf), figsize=(15, 6))
    fig.subplots_adjust(wspace=.3, hspace=.2, bottom=.2, top=.9)
    axs.ravel()

    # adding caption
    plt.figtext(0.5, 0.01, caption, wrap=True, ha='center', va='bottom', fontsize=10, fontstyle='italic')

    # allocating for residual error
    cost = np.zeros((len(SNR), len(cf), len(ln)))
    residual = []

    # Creating copies of data to alter
    dx = datax.copy()
    dy = datay.copy()

    # TODO: cross validate optimal f scale
    f_scale = [5e-3, 1e-6, 1e-3]

    # standard colors
    prop_cycle = plt.rcParams['axes.prop_cycle']
    colors = prop_cycle.by_key()['color']

    # Doing regression
    for k, ratioInds in enumerate(SNR):  # for each signal to noise ratio
        for i, curve in enumerate(cf):  # for each NLS problem

            durSpan = np.linspace(min(dx[i]), max(dx[i]), 1000,
                                  endpoint=True)  # x-values for our smooth regression curves

            # plotting the binned/averaged ground truth
            if baseplot[i] == 'hist':  # if histogram
                axs[i].hist(groundtruth[i], bins=180, align='mid', histtype='stepfilled', color=colors[-1])

            else:  # if scatter plot
                dx[i] = datax[i][ratioInds]
                dy[i] = datay[i][ratioInds]

                errorbs = np.ones(len(durInd))
                ERxPT = np.ones(len(durVal))  # MAE, by visualization durations
                for j, y in enumerate(durVal):
                    SNRxPT = list(set(ratioInds) & set(durInd[y][0]))  # indices for trials with specified SNR and PT
                    ERxPT[j] = abs_err(est_mu[SNRxPT], res_mu[SNRxPT]).mean()
                    ERxSNRxPT = allER[SNRxPT]
                    errorbs[j] = scipy.stats.sem(ERxSNRxPT)  # standard error of the mean

                groundtruth[i] = ERxPT  # redefining groundtruth with "SNR-filter"

                axs[i].plot(np.unique(dx[i]), groundtruth[i], 'o', c=colors[k])

                # plotting error bar if it's called for
                if errorbar:
                    axs[i].errorbar(np.unique(dx[i]), groundtruth[i], yerr=errorbs[k], fmt='none', c=colors[k])

            # fitting our curve and plotting
            for j, loss in enumerate(ln):
                if loss == 'linear':
                    fit_curve = least_squares(lf[i], fit_x0[i], loss=loss, args=(dx[i], dy[i]), verbose=2)
                else:
                    fit_curve = least_squares(lf[i], fit_x0[i], loss=loss, f_scale=f_scale[i],
                                              args=(dx[i], dy[i]), verbose=1, ftol=1e-11, xtol=1e-11,
                                              gtol=1e-11,
                                              jac='cs')  # bounds=bounds[i], method='dogbox')  # how to choose ideas f_scale?

                y_fit_lsq = curve(durSpan, [*fit_curve.x])

                # Plotting, with correct labels
                if test:
                    axs[i].plot(durSpan, y_fit_lsq, label=loss, alpha=.8)
                else:
                    if baseplot[i] == 'scatter':
                        axs[i].plot(durSpan, y_fit_lsq, label=f'{SNRstr[k]}', alpha=.8, c=colors[k])
                    else:
                        axs[i].plot(durSpan, y_fit_lsq, alpha=.8, c=colors[k])

                axs[i].set_xlabel(xlabels[i])
                axs[i].set_ylabel(ylabels[i])
                axs[i].set_title(cn[i])
                axs[i].legend()

                # adding figure labels
                figlabs = ['a', 'b', 'c', 'd']
                axs[i].text(.12, 1.06, figlabs[i], transform=axs[i].transAxes,
                            fontsize=14, va='top', ha='right')

                # saving residual error for each combination of curve-loss
                residual.append(fit_curve.fun)  # ordered by losses, curves, then SNR ratios
                cost[k, i, j] = fit_curve.cost

                # TODO: Save CI, p-value, coefficient for reporting

                # residual[i, j] = fit_curve.optimality # In unconstrained problems, it is always the uniform norm of the
                # gradient. In constrained problems, it is the quantity which was compared with gtol
                # residual[i, j] = ss_res(ERxPT, y_fit_lsq[durVal.astype(int)])

    fig.show()

    return cost, residual  # cost is SNR x fitted function x loss function
