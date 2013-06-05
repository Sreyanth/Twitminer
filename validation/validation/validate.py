# 
# Tests your models against by using 25% of the training data
# as validation data.
#

import pdb
from models import lol
from models import bayes
from models import gaussian
from models import sgd
from models import decisiontree
from models import randomforest
from models import bayes_mod
import random
from features import *
import csv

RESULTS = "tmp/validation"

SPORTS_FOR_SURE_TAGS = ["olympic", "f1", "cricket", "ball", "wicket", "umpire", "soccer", "aussie", 
                        "ranji ", "ganguly ", "tendulkar ", "sport", "bcci", "tennis", "worldcup",
                        "champions league", " cup ", "indvaus", "bcci", "fifa", "badminton", "hockey",
                        "fedcup", "usopen", "federer", "nadal", "motogp", "ausgp", "forceindia",
                        "ticket", "stadium", "grandprix", "chelsea", "bowl", "fielder", "runs",
                        "dhoni", "innings", "wimbledon", "singles", "doubles", " team ", "sochi2014",
                        "semifinal", "sail", " medal"]

POLITICS_FOR_SURE_TAGS = ["obama", "medvedev", "manmohan", "minist", "president", "parliament", "politic",
                          "conference", "peace", "nelson", "secretar", "cabinet", "barack", "econom", "budget",
                          "govern", "violen", "pmoindia", "tax", "debat", "statement", "speech", "educat",
                          "society", "govt", "business", "ambassador", "lincoln"]


models_to_test = {
    #"lol": lol,
    # "decisiontree" : decisiontree, 
    # "bayes": bayes,
    # "gaussian" : gaussian, 
    # "sgd" : sgd,
    # "randomforest" : randomforest,
    # "gmm" : gmm, 
    "bayes_mod" : bayes_mod
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
    towrite = []
    right = 0
    print "Validating."
    for t in validation_set:
        flag = True

        for word in SPORTS_FOR_SURE_TAGS:
            if word in t["ttext"].lower():
                cls = 2
                info = "write"
                flag = False
                break

        if flag:
            for word in POLITICS_FOR_SURE_TAGS:
                if word in t["ttext"].lower():
                    cls = 1
                    info = "write"
                    flag = False
                    break
        if flag:
            cls = model.classify(tweet_vector(t))
            try:
                cls, info = cls
            except: info = ''

        if info == "write":
            towrite.append(t["id"]+" "+get_class_name(cls)+" "+t["ttext"])

        #info += [" ".join(t["all"])]
        result.append([
            t["id"],
            get_class_name(cls),
            t["ttext"]#,
            #" ".join(t["all"])
            ])
    return result, towrite

print "Preparing..."

X, Y = getXY(training_set)
for name in models_to_test:
    result, towrite = test_model(name, models_to_test[name])

    lines = []
    with open(RESULTS + "/%s_info.txt" % name, "w") as f:
        for row in result:
            lines.append(" ".join(row))
        f.writelines(lines)
        f.close()

    with open(RESULTS + "/%s_add.txt" % name, "w+") as f:
        f.writelines(towrite)
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
