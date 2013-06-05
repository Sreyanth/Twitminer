#!/usr/bin/env python

"""
#-------------------------------------------------------------------------------
# Name:        test.py
# Purpose:     This is the main script which handles the entire testing part
#              The model is built, trained and used for predictions on the
#              testing data.
#
# Author:      Shashi Gowda and M Sreyantha Chary
#
# Created:     03/03/2013
# Copyright:   (c) Shashi & Sreyantha Chary 2013
# Licence:     Open for anyone to use! If you find any bug, let us know
#              at shashi@nitk.ac.in or sreyanth@gmail.com
#-------------------------------------------------------------------------------
"""

import pdb
from models import CustomizedBayes
import random
from features import *
import csv

RESULTS = "tmp/results"

# These tags, if found, are for sure sports! Determined from stats.
# Also some manual additions after googling for top trends.
#
# Can we use?
# Yes, you can use any synonymous words while learning
# (reply via email to one of our queries)
#

SPORTS_FOR_SURE_TAGS = [' cup ',
                        'athlete',
                        'ausgp',
                        'aussie',
                        'badminton',
                        'ball',
                        'bcci',
                        'bowl',
                        'champions league',
                        'chelsea',
                        'cricket',
                        'dhoni',
                        'doubles',
                        'f1',
                        'fedcup',
                        'federer',
                        'fielder',
                        'fifa',
                        'forceindia',
                        'ganguly ',
                        'grandprix',
                        'hockey',
                        'indvaus',
                        'innings',
                        'motogp',
                        'nadal',
                        'olympic',
                        'ranji ',
                        'runs',
                        'sail',
                        'semifinal',
                        'singles',
                        'soccer',
                        'sochi',
                        'sport',
                        'stadium',
                        'tendulkar ',
                        'tennis',
                        'ticket',
                        'umpire',
                        'usopen',
                        'wicket',
                        'wimbledon',
                        'worldcup']

# These tags, if found, are for sure politics! Determined from stats.
# Also some manual additions after googling for top trends.
#
# Can we use?
# Yes, you can use any synonymous words while learning
# (reply via email to one of our queries)
#

POLITICS_FOR_SURE_TAGS = ['ambassador',
                          'barack',
                          'budget',
                          'business',
                          'cabinet',
                          'conference',
                          'debat',
                          'econom',
                          'educat',
                          'govern',
                          'govt',
                          'lincoln',
                          'manmohan',
                          'medvedev',
                          'minist',
                          'nelson',
                          'obama',
                          'parliament',
                          'peace',
                          'pmoindia',
                          'politic',
                          'president',
                          'secretar',
                          'society',
                          'speech',
                          'statement',
                          'tax',
                          'violen']

# This enables us to quickly add, delete models!
models_to_test = {
    "CustomizedBayes" : CustomizedBayes
}

#
# Test a model.
#
# args:
#   - name: a name for the model
#   - model: the model's module
#

# Function that takes an integer and returns appropriate label
def get_class_name(cls):
    if cls == 1: return "Politics"
    else: return "Sports"

# Function to start testing using model
def test_model(name, model):
    print "Testing model", name
    model.clear()   # Initialise the model


    print "Training."
    model.fit(X, Y) # Fit the training data

    result = []     # list containing the results
    towrite = []    # List containing the probable correctly labelled tweets
                    # so that if continous learning is used, will be useful

    print "Testing!."
    for t in test_set:

        flag = True # flag to check if the tweet falls under FOR SURE category

        for word in SPORTS_FOR_SURE_TAGS:
            if word in t["ttext"].lower():
                cls = 2
                info = "write"
                flag = False
                break

        # There may be some tweets where both the types of FOR_SURE_TAGS are present. We just
        # Assign them as sports!
        
        if flag:
            for word in POLITICS_FOR_SURE_TAGS:
                if word in t["ttext"].lower():
                    cls = 1
                    info = "write"
                    flag = False
                    break

        if flag:    # tweet isnt in FOR SURE category. Send it to the classifier
                    # Let it predict!
            cls = model.classify(tweet_vector(t))
            try:
                cls, info = cls
            except: info = ''

        if info == "write":
            towrite.append(t["id"]+" "+get_class_name(cls)+" "+t["ttext"])

        result.append([
            t["id"],
            get_class_name(cls),
            t["ttext"]
            ])

    return result, towrite


print "Preparing..."

X, Y = getXY(training_set)
for name in models_to_test:
    result, towrite = test_model(name, models_to_test[name])

    lines = []
    with open(RESULTS + "/%s_info.txt" % name, "w") as f:
        # Contains the <tweetid> <predicted_label> <tweet_text>
        for row in result:
            lines.append(" ".join(row))
        f.writelines(lines)
        f.close()

#    with open(RESULTS + "/continuous.txt" % name, "w+") as f:
#       # Can be used if continuous learning is made use of.
#       # To use for it, we will have to add some lines to features.py
#
#       f.writelines(towrite)
#      f.close()


    # Generating the results in <tweetid> <predicted_label> format to upload
    lines = []
    with open(RESULTS + "/%s.txt" % name, "w") as f:
        for row in result:
            lines.append(" ".join(row[0:2]) + "\n")
        f.writelines(lines)
        f.close()
