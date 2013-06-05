import pdb
import numpy as np
from sklearn.naive_bayes import MultinomialNB

classifier = {}
ftypes = ["keywords", "hashtags", "urls", "refs", "all"]

def clear():
    for ftype in ftypes:
##        classifier[ftype] = MultinomialNB(alpha=0.7, fit_prior=False) 91.29827
##        classifier[ftype] = MultinomialNB(alpha=0.65, fit_prior=False) 91.39134
##        classifier[ftype] = MultinomialNB(alpha=0.6, fit_prior=False) 91.34481
##        classifier[ftype] = MultinomialNB(alpha=0.675, fit_prior=False) 91.34481
        classifier[ftype] = MultinomialNB(alpha=0.635, fit_prior=False)

def fit(X, Y):
    for ftype in ftypes:
        classifier[ftype].fit(X[ftype], Y[ftype])

def classify(X):
    weights = {
        "keywords": 3,
        "hashtags": 5,
        "urls": 1,
        "refs": 2,
        "all": 11
    }

##    remark = [str(p) for p in classifier["all"].predict_proba(X["all"])[0]]
##
##    return [classifier["all"].predict(X["all"]), remark]
    wsum = 0
    weight = 0
    for ftype in ftypes:
        if len(X[ftype])!=0:
            wsum += weights[ftype] * classifier[ftype].predict(X[ftype])
            weight += weights[ftype]

    if (round(wsum)/round(weight)) >= 1.5:
        return 2
    else:
        return 1
