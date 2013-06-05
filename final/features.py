#!/usr/bin/env python

"""
#-------------------------------------------------------------------------------
# Name:        features.py
# Purpose:     Extracting features from tweets and making them ready for
#              our purpose. Both training and test data are handled.
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
import re
import csv
import numpy as np
import random
from stemmer import PorterStemmer

__all__ = [
    "training_set",     # This set contains all the training data
    "getXY",            # This function gets the vectors of all the features.
    "idtable",          # The id table dict we use to build the vectors
    "tweet_vector",     # This function takes a tweet and vectorizes it
    "test_set",         # This set contains all the test data
    "SPORTS",           # SPORTS variable, an integer, we take it as 2
    "POLITICS",         # POLITICS variable, an integer, we take it as 1
    "get_features"      # The function which takes care of getting features.
    ]

# Defining the Datasets, first folder, then files
DATASETS = "datasets"   # Datasets folder
TRAINING = DATASETS + "/training.txt"
TEST = DATASETS + "/test.txt"

# Defining the variables, for training!
SPORTS = 2
POLITICS = 1

# Regexes used to extract features from tweets
HASHTAGS = re.compile("\#([^\s\,\.\#\"\'\+\=\|\$\%\^\:]+)") # Extracts #tags
URLS1 = re.compile("https?\:\/\/([^\s]+)")  # Extracts URLs of type: http/https:
URLS2 = re.compile("www\.([^\s]+)") # Extracts URLs like www.google.com
REFS = re.compile("\@([^\s\,\.\#\"\'\+\=\|\$\%\^\:\-]+)") # Extracts @rep/mentions
KEYWORDS = re.compile("(\w+)")  # Extracts keywords from the tweet text!
WHITESPACE = re.compile("[\s\.\,\'\"\[\]\{\}\;\:\/\&\=\+\-\)\(\*\&\^\%\$\`\|\?\!]+")

# Initialising the Stemmer!
STEMMER = PorterStemmer()

# Initialising our idtable dict.
idtable = {}

# Function which returns the id of a key in a given table.
def get_id(table, key, write=True):
    if table.has_key(key): return table[key]
    else:
        if write:
            table[key] = len(table)
            return table[key]
        else:
            return None

# Function to register keys in the table.
def register(table, keys, write=True):
    return [get_id(table, k, write) for k in keys]

# Function to split names and to extract abbreviations
def split_unames(txt):
    extended = []
    NAME = "[A-Z][a-z0-9]+" # Regex to match a name
    ABBR = "([A-Z]+)[A-Z_]" # Regex to match an abbreviation

    n = re.compile(NAME)
    a = re.compile(ABBR)

    for tmp in txt:
        abbrs = a.findall(tmp)
        tmp = tmp.replace("_", "")

        s = n.findall(tmp)
        s_ = [i.split('_') for i in s]

        s = [tmp] + abbrs
        for i in s_:
            s += i
        extended += s
    extended = remove_stopwords(extended)
    return extended

# Function which takes the dataset and returns the feature vectors
def getXY(dataset):
    # dataset => A dataset with extracted features

    X = {}
    Y = {}

    for ftype in ["keywords", "hashtags", "urls", "refs", "all"]:

        # keywords  => keywords extracted
        # hashtags  => hashtags extracted
        # urls      => URLs extracted
        # refs      => @refs extracted
        # all       => all the above info!!

        X[ftype] = []
        Y[ftype] = []
        tmp = []
        idtable[ftype] = {}
        for d in dataset:
            if len(d[ftype])!=0:
                tmp.append(register(idtable[ftype], d[ftype]))
                Y[ftype].append(d["label"])

        # you have tmp[ftype] populated with ids of the features present

        n = len(idtable[ftype])
        for idset in tmp:
            vector = [0] * n
            for i in idset:
                try:
                    vector[i] = 1
                except: print i, n
            X[ftype].append(vector)

        X[ftype] = np.array(X[ftype])
        Y[ftype] = np.array(Y[ftype])
    return X, Y

# Function to vectorize a given tweet! This is used for the test tweets.
def tweet_vector(tweet):
    tv = {}
    for ftype in ["keywords", "hashtags", "urls", "refs", "all"]:

        # keywords  => keywords extracted
        # hashtags  => hashtags extracted
        # urls      => URLs extracted
        # refs      => @refs extracted
        # all       => all the above info!!

        ids = register(idtable[ftype], tweet[ftype], False)
        n = len(idtable[ftype])
        vector = [0] * n
        for id in ids:
            if id == None: continue # unseen values! <-- do something maybe?
            vector[id] = 1
        tv[ftype] = vector

    return tv

# Function to remove stop words
def remove_stopwords(words):
    swords = set([w.strip() for w in open("stopwords.txt").readlines()])
    wset = set(words)
    return list(wset.difference(swords))

# Function that takes the label, and returns the integer accordingly
def get_class(label):
    l = label.strip().lower()
    if l == "sports": return SPORTS
    if l == "politics": return POLITICS

# Function which extracts the features from the datasets!
def get_features(id, ttext, label=None):

    # the order in which features should be extracted:
    #
    # hashtags
    # urls
    # @-replys
    # keywords

    tmp = ttext

    hashtags = HASHTAGS.findall(ttext)
    hashtags = split_unames(hashtags)
    ttext = HASHTAGS.sub("", ttext)

    urls = URLS1.findall(ttext)
    ttext = URLS1.sub("", ttext)

    urls += URLS2.findall(ttext)
    ttext = URLS2.sub("", ttext)

    refs = REFS.findall(ttext)
    ttext = REFS.sub("", ttext)
    refs = split_unames(refs)

    keywords = WHITESPACE.split(ttext.lower())
    keywords = remove_stopwords(keywords)

    def lowercase(l): return [i.lower() for i in l]
    def stem(l): return [STEMMER.stem(w, 0, len(w) -1) for w in l]

    all = stem(lowercase(keywords +hashtags + urls + refs))
    try:
        while 1:
            all.remove("")
    except ValueError: pass

    # These are the extracted info!
    #   {
    #       "id" : id_number
    #       "label" : 1 or 2 or None depending on if it is Politics or Sports or Test
    #       "ttext" : The original tweet text
    #       "all" : list of all the extracted feature items
    #       "keywords" : list of Extracted Keywords
    #       "hashtags" : list of Extracted Hashtags
    #       "urls" : list of Extracted URLs
    #       "refs" : list of Extracted @replys
    #   }
    #

    features = {
        "id": id,
        "label": label,
        "ttext": tmp,
        "all": all,
        "keywords": keywords,
        "hashtags": lowercase(hashtags),
        "urls": urls,
        "refs": refs
    }

    return features

##################  BUILDING THE TRAINING AND TEST DATA SETS    ###################

training_set = []
data = []

with open(TRAINING) as f:
    data = [l.split(' ', 2) for l in f.readlines() ] # Assumes the format is followed
    for row in data:
        fs = get_features(row[0], row[-1], get_class(row[1]))
        training_set.append(fs)

# try:
#     # Should be uncommented, only if we are using coninuous learning
#     with open("tmp/results/continuous.txt") as f:
#         data = [l.split(' ', 2) for l in f.readlines() ] # Assumes the format is followed
#         for row in data:
#             fs = get_features(row[0], row[-1], get_class(row[1]))
#             training_set.append(fs)
# except:
#     pass

random.shuffle(training_set)    # Shuffling the training set
                                # Though the training data is already shuffled
                                # Just to make sure of it again

test_set = []

with open(TEST) as f:
    for line in f.readlines():
        info = line.split(' ', 1)
        fs = get_features(info[0], info[-1])
        test_set.append(fs)
