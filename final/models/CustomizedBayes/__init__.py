#!/usr/bin/env python

"""
#-------------------------------------------------------------------------------
# Name:        __init__.py
# Purpose:     This is the main script for Customized Bayes.
#              5 classifiers, one each for each ftype will be built
#              and weighted prediction is done.
#
# Author:      Shashi Gowda and M Sreyantha Chary
#
# Created:     14/03/2013
# Copyright:   (c) Shashi & Sreyantha Chary 2013
# Licence:     Open for anyone to use! If you find any bug, let us know
#              at shashi@nitk.ac.in or sreyanth@gmail.com
#-------------------------------------------------------------------------------
"""

import pdb
import numpy as np
from sklearn.naive_bayes import MultinomialNB

# Initialse the classifiers dict
classifier = {}
ftypes = ["keywords", "hashtags", "urls", "refs", "all"]

def clear():

    # Initializing the classifiers. We will have 5, one for each ftype

    for ftype in ftypes:

        # After testing and tuning on the validation set, we have chosen
        # the alpha value to be 0.65 and fit_prior = True
        # More about alpha and fit_prior on scikit's documentation

        classifier[ftype] = MultinomialNB(alpha = 0.65, fit_prior = True)

def fit(X, Y):

    # Fitting the training data into the respective classifier

    for ftype in ftypes:
        classifier[ftype].fit(X[ftype], Y[ftype])

def classify(X):

    # X is the tweet vector of a tweet

    weights = {

    # weights assigned for each ftype.
    # Done after a lot of experimentation

        "keywords": 3,
        "hashtags": 6,
        "urls": 1,
        "refs": 2,
        "all": 11
    }

    wsum = 0    # The weighted sum
    weight = 0  # The sum of relevant weights

    for ftype in ftypes:
        if len(X[ftype])!=0:
            wsum += weights[ftype] * classifier[ftype].predict(X[ftype])
            weight += weights[ftype]

    result = (round(wsum)/round(weight))    # A floating point helping us to
                                            # choose appropriate classs

    write = ''

    if result <= 1.25 or result >= 1.75:

        # Just to use incase, continous learning is used
        # Which means, the probably correctly classified
        # tweets can be used as training supplement in the
        # next classification!

        write = "write"

    if result >=1.45:
        # 1.45 is chosen after fine tuning wrt validation results
        # and wrt the weights.

        return 2, write
    else:
        return 1, write
