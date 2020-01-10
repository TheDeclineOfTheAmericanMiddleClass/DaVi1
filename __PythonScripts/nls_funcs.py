import numpy as np


# Exponential function and loss
def exp_lossfunc(x, t, y):  # loss function for our exponential a + b*(c*t)
    return x[0] + x[1] * np.exp(x[2] * t) - y


def expfunc(t, x):  # takes vector of values for a, b, c in y = a + b*(c*t)
    return x[0] + x[1] * np.exp(x[2] * t)


# 4 param logistic function and loss
def four_lossfunc(x, t, y):  # loss function for our four param logistic
    return (x[3] + (x[0] - x[3]) / (1 + (t / x[2])) ** x[1]) - y


def fourfunc(t, x):  # takes vector of values for a, b, c, d  in y = d + (a-d) / (1 + t/c)**b
    return x[3] + (x[0] - x[3]) / (1 + (t / x[2])) ** x[1]


# defining gamma distibution
import scipy.special as spec


def gdfunc(t, x):
    return x[2] * (
            t ** (x[0] - 1) * np.exp(-t / x[1]) / (x[1] ** x[0] * spec.gamma(x[0])))  # x = [shape k, scale theta]


def gd_lossfunc(x, t, y):
    return x[2] * (t ** (x[0] - 1) * np.exp(-t / x[1]) / (x[1] ** x[0] * spec.gamma(x[0]))) - y


# residual sum of squares
def ss_res(y, y_fit):
    np.sum((y - y_fit) ** 2)


# total sum of squares
def ss_tot(y):
    np.sum((y - np.mean(y)) ** 2)


# r-squared
def r2(y, y_fit):
    return 1 - (ss_res(y, y_fit) / ss_tot(y, y_fit))
