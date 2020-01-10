from scipy.optimize import least_squares
import matplotlib.pyplot as plt
from __PythonScripts.read_data import *


# Testing different lossnames and plotting various curve functions in loop
def NLSfit(datax, datay, fit_x0, cn, cf, ln, lf, groundtruth, xlabels, ylabels, errorbs, baseplot='scatter'):
    """Takes arrays of each of the following: type of loss, curve function to fit, name of curve function,
    and initial conditions for each type of curve """

    # setting up figure
    fig, axs = plt.subplots(1, len(cf), figsize=(10, 4))
    fig.subplots_adjust(wspace=.3, hspace=.2)
    axs.ravel()

    residual = np.zeros((len(cf), len(ln)))  # allocating residual error

    # todo: cross validate optimal f scale
    f_scale = [5e-3, 1e-6, 1e-3]

    # doing regression
    for i, curve in enumerate(cf):
        durSpan = np.linspace(min(datax[i]), max(datax[i]), 1000,
                              endpoint=True)  # x-values for our smooth regression curves

        # plotting the binned/averaged ground truth
        if baseplot[i] == 'hist':
            axs[i].hist(groundtruth[i], bins=180, align='mid', histtype='step')
        else:
            axs[i].plot(np.unique(datax[i]), groundtruth[i], 'o')
            axs[i].errorbar(np.unique(datax[i]), groundtruth[i], yerr=errorbs[i], fmt='none')

        # plotting our curve fit
        for j, loss in enumerate(ln):
            if loss == 'linear':
                fit_curve = least_squares(lf[i], fit_x0[i], loss=loss, args=(datax[i], datay[i]), verbose=2)
            else:
                fit_curve = least_squares(lf[i], fit_x0[i], loss=loss, f_scale=f_scale[i],
                                          args=(datax[i], datay[i]), verbose=1, ftol=1e-11, xtol=1e-11,
                                          gtol=1e-11,
                                          jac='cs')  # bounds=bounds[i], method='dogbox')  # how to choose ideas f_scale?

            y_fit_lsq = curve(durSpan, [*fit_curve.x])

            # plotting
            axs[i].plot(durSpan, y_fit_lsq, label=loss, alpha=.8)
            axs[i].set_xlabel(xlabels[i])
            axs[i].set_ylabel(ylabels[i])
            axs[i].set_title(cn[i])
            axs[i].legend()

            # print(fit_curve.cost)
            # saving residual error for each combination of curve-loss
            residual[i, j] = fit_curve.cost
            # residual[i, j] = fit_curve.optimality # In unconstrained problems, it is always the uniform norm of the
            # gradient. In constrained problems, it is the quantity which was compared with gtol
            # residual[i, j] = ss_res(ERxPT, y_fit_lsq[durVal.astype(int)])

    fig.show()

    return residual
