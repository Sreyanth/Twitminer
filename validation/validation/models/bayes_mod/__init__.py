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
##        classifier[ftype] = MultinomialNB(alpha=0.65, fit_prior=True) 93.34 for the validation_learnt!
##        classifier[ftype] = MultinomialNB(alpha = 1.4, fit_prior= True) 93.992
##        classifier[ftype] = MultinomialNB(alpha = 1.6, fit_prior= True) 94.09
##        classifier[ftype] = MultinomialNB(alpha = 1.5, fit_prior= False) 95.57 on added one!
##        Just learnt that the alpha value is normally chosen less than 1 !!!
        classifier[ftype] = MultinomialNB(alpha = 0.65, fit_prior= True)

def fit(X, Y):
    for ftype in ftypes:
        classifier[ftype].fit(X[ftype], Y[ftype])

def classify(X):
    weights = {
        "keywords": 3,
        "hashtags": 6,
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

    result = (round(wsum)/round(weight))

    write = ''
    
    if result <= 1.3 or result >= 1.7:
        write = "write"
    if result >=1.45:
        return 2, write
    else:
        return 1, write
