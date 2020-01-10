from __PythonScripts.pilot_stats import *


def summary_stats():
    ## Error values of interest
    print(f'\nMean Absolute Error, cardinal directions: {avgERxCard:.4}, pad: +/-{card_pad:.4} radians',
          f'\nMean Absolute Error Error, oblique directions: {avgERxObli:.4}, pad: +/-{obli_pad:.4} radians',
          # f'\nNon-oblique/cardinal Error: {nonOC_Err:.02}'
          f'\nTotal Mean Absolute Error: {avgERxTrials:.02}')

    # Percent more cardinal vs. oblique presentations
    CvO_percent = (len(cardinalTrials) - len(obliqueTrials)) / (len(cardinalTrials) + len(obliqueTrials))
    print(f'\nCardinal presentations: {len(cardinalTrials)}\n'
          f'Oblique presentations: {len(obliqueTrials)}\n'
          f'Percent more obli than card: {CvO_percent:.03}')

    print(f'\nMean RT for cardinal mu {avgRTxCard:.2f}'
          f' \nMean RT for oblique mu is {avgRTxObli:.2f}\n')

    for i, x in enumerate(prop_RT_mean):
        print(f'Average response time for propmix {propVal[i]} is {prop_RT_mean[i]:.2f} ms')

    # print(f'\nEstimated vs. theoretical parameters: \nmu MSE is {mu_MSE},\nkappa MSE is {kappa_MSE}')
