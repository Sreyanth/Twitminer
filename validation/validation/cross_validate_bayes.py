#
# Tests your models against by using 25% of the training data
# as validation data.
#

import pdb

from models import bayes

import random
from features import *
import csv

RESULTS = "tmp/validation"

models_to_test = {
    "bayes": bayes
}

#
# Test a model.
#
# args:
#   - name: a name for the model
#   - model: the model's module
#

def get_class_name(cls):
    if cls == 1: return "Politics"
    else: return "Sports"

def test_model(name, model):
    print "Testing model", name
    model.clear()


    print "Training."
    model.fit(X, Y)

    result = []
    error = []
    right = 0
    print "Validating."
    for t in training_set:
        cls = model.classify(tweet_vector(t))
        try:
            cls, info = cls
        except: info = []

        #info += [" ".join(t["all"])]
        result.append([
            t["id"],
            get_class_name(cls),
            t["ttext"],
            " ".join(t["all"])
            ])
        if t["label"]!=cls:
            error.append([
            t["id"], get_class_name(t["label"]),
            get_class_name(cls),
            t["ttext"],
            " ".join(t["all"])
            ])
    return result, error

print "Preparing..."

X, Y = getXY(training_set)
for name in models_to_test:
    result, error = test_model(name, models_to_test[name])

    lines = []
    with open(RESULTS + "/%s_info.txt" % name, "w") as f:
        for row in result:
            lines.append(" ".join(row) + "\n")
        f.writelines(lines)
        f.close()

    errors = []
    with open(RESULTS + "/%s_errors.txt" % name, "w") as f:
        for row in error:
            errors.append(" ".join(row) + "\n")
        f.writelines(errors)
        f.close()

    # add 20% random results
    lines = []
    with open(RESULTS + "/%s.txt" % name, "w") as f:

        l = len(result)
        nums = range(0, len(result))
        random.shuffle(nums)
##        for i in nums[int(.9*l):]:
##            result[i][1] = random.choice(["Sports", "Politics"])

        for row in result:
            lines.append(" ".join(row[0:2]) + "\n")
        f.writelines(lines)
        f.close()
