import pdb
import numpy as np
from sklearn.tree import DecisionTreeClassifier
classifier = {}
def clear(): classifier["all"]= DecisionTreeClassifier(criterion='gini', max_depth=None,
                                                min_samples_split=2, min_samples_leaf=1,
                                                min_density=0.10000000000000001, max_features=None,
                                                compute_importances=True, random_state=None)

def fit(X, Y): classifier["all"].fit(X["all"], Y["all"])

def classify(X): return [classifier["all"].predict(X["all"]), [str(p) for p in classifier["all"].predict_proba(X["all"])[0]]]

