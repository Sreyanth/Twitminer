# 
# Tests your models against by using 25% of the training data
# as validation data.
#

import pdb
from models import lol
from models import bayes
from features import *
import csv

RESULTS = "tmp/results"

models_to_test = {
    "lol": lol,
    "bayes": bayes
}

#
# Test a model.
#
# args:
#   - name: a name for the model
#   - model: the model's module
#
    
def test_model(name, model):
    print "Testing model", name
    model.clear()


    print "Training."
    model.fit(X, Y)

    result = []
    right = 0
    print "Validating."
    for t in training_set_25pc:

        cls = model.classify(tweet_vector(t))
        try:
            cls, info = cls
        except: info = []

        info += [" ".join(t["all"])]
        assertion = bool(cls == t["label"])
        result.append([
            t["id"],
            ["wrong", "right"][assertion],
            cls,
            t["label"],
            t["ttext"],
            ] + info)
        if assertion: right += 1

    accuracy = right / (1.0 * len(result))

    return result, accuracy

print "Preparing..."

X, Y = getXY(training_set_75pc)
for name in models_to_test:
    result, accuracy = test_model(name, models_to_test[name])
    print "%s: %f" % (name, accuracy)

    with open(RESULTS + "/%s.csv" % name, "w") as csvfile:
        writer = csv.writer(csvfile, delimiter=",", quotechar='"')
        for row in result:
            writer.writerow(row)

        csvfile.close()
