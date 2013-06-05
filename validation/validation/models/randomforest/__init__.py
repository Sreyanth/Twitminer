import pdb
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import scipy

classifier = {}
#ftypes = ["keywords", "hashtags", "urls", "refs", "all"]
ftypes = ["all"]

def clear():
    for ftype in ftypes:
        classifier[ftype] = RandomForestClassifier()

def fit(X, Y):
    for ftype in ftypes:
        print "Training on %s" % (ftype)
        classifier[ftype].fit(X[ftype], Y[ftype])

def classify(X):
    weights = {
        "keywords": 1,
        "hashtags": 4,
        "urls": 4,
        "refs": 1,
        "all": 8
    }

    remark = [str(p) for p in classifier["all"].predict_proba(X["all"])[0]]

    return [classifier["all"].predict(X["all"]), remark]
    wsum = 0
    for ftype in ftypes:
        wsum += weights[ftype] * classifier[ftype].predict(X[ftype])

    return int(round(wsum / sum(weights.values())))
