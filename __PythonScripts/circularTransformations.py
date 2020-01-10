import numpy as np


# Converting cartesian coordinates to radians, with zero radians at 90 cartesian degrees (aka x = 0, y = +inf)
def cart2pol(x, y):
    """Converts cartesian to polar coordinates, where phi is the angle of difference
    of a ray from origin to (0,1) and a ray from the origin to the given cartesian coordinates.

    Credit: https://stackoverflow.com/questions/20924085/python-conversion-between-coordinates"""

    r = np.sqrt(x ** 2 + y ** 2)
    phi = -np.arctan2(y, x)

    # adjustments, given circularity # TODO: understand why this works
    phi += np.pi / 2
    phi[phi < 0] += 2 * np.pi

    return r, phi


def pol2cart(r, phi):
    """Converts polar coordinates to cartesian, with 0 rad at (1,0)
    NO CONVERSION INTO EXPERIMENT CARTESIAN PLANE"""

    x = r * np.cos(phi)
    y = r * np.sin(phi)

    return x, y


# Unsigned radial angle difference
def ang_diff(a1, a2):
    """Takes array of radians of two points on a circle.
    Returns absolute distance between them, in radians."""

    r1, p1 = cart2pol(pol2cart(1, a1)[0], pol2cart(1, a1)[1])
    r2, p2 = cart2pol(pol2cart(1, a2)[0], pol2cart(1, a2)[1])

    diff = np.abs(p1 - p2)
    diff[diff > np.pi] -= np.pi

    # TODO: determine if there is a problem with pi/2
    return diff


# TODO: edit signed_ang_diff as ang_diff
# def signed_ang_diff(a1, a2):
#     """Takes angular polar coordinate of two points on a circle.
#     Returns signed angular distance."""
#
#     diff = a1 - a2
#     diff[diff > np.pi] -= np.pi
#     diff[diff < -np.pi] += np.pi
#
#     return diff

# Angular error function
def ang_err(a, b):
    """ Calculates angular distance between two arrays holding radian coordinates.
    Return distance as percentage of maximum distance between any 2 points on circle."""
    return 100 * np.arctan2(np.sin(a - b), np.cos(a - b)) / np.pi


def abs_err(a, b):
    """ Calculates angular distance between two arrays holding radian coordinates.
    Returns distance in absolute degrees"""
    return np.abs(np.arctan2(np.sin(a - b), np.cos(a - b)) * 360 / (2 * np.pi))


# Defining function to specify indices in angular window of interest
def circ_window(doi, est_mu, pad=np.pi / 16):
    """This function takes array of directions of interest, a user-generated name for indices, and padding around
    each direction.

    Returns indices for that window of interest."""
    ind = np.empty(0)

    for i, direc in enumerate(doi):
        lo_bound = np.where(est_mu < (direc + pad))[0]
        hi_bound = np.where(est_mu > (direc - pad))[0]
        ind = np.hstack((ind, np.intersect1d(lo_bound, hi_bound)))

    return ind.astype('int')

# TODO: Change script to accommodate est_mu outside of function
