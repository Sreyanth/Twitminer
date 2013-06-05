import pdb
import numpy as np
from sklearn.linear_model import SGDClassifier

classifier = {}
ftypes = ["keywords", "hashtags", "urls", "refs", "all"]

def clear():
    for ftype in ftypes:
        classifier[ftype] = SGDClassifier(loss="modified_huber", penalty="l2")

def fit(X, Y):
    for ftype in ftypes:
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
