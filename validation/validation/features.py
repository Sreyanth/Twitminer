import pdb
import re
import csv
import numpy as np
import random
from stemmer import PorterStemmer

__all__ = [
    "training_set",
    "training_set_75pc",
    "training_set_25pc",
    "getXY",
    "idtable",
    "tweet_vector",
    "validation_set",
    "validation_set_large",
    "validation_set_small",
    "SPORTS",
    "POLITICS",
    "get_features"
    ]

DATASETS = "datasets"
TRAINING = DATASETS + "/training.txt"
VALIDATION = DATASETS + "/validation.txt"

SPORTS = 2
POLITICS = 1

HASHTAGS = re.compile("\#([^\s\,\.\#\"\'\+\=\|\$\%\^\:]+)")
URLS1 = re.compile("https?\:\/\/([^\s]+)")
URLS2 = re.compile("www\.([^\s]+)")
REFS = re.compile("\@([^\s\,\.\#\"\'\+\=\|\$\%\^\:\-]+)")
KEYWORDS = re.compile("(\w+)")
WHITESPACE = re.compile("[\s\.\,\'\"\[\]\{\}\;\:\/\&\=\+\-\)\(\*\&\^\%\$\`\|\?\!]+")
STEMMER = PorterStemmer()

idtable = {}

def get_id(table, key, write=True):
    if table.has_key(key): return table[key]
    else:
        if write:
            table[key] = len(table)
            return table[key]
        else:
            return None

def register(table, keys, write=True):
    return [get_id(table, k, write) for k in keys]

def split_unames(txt):
    extended = []
    NAME = "[A-Z][a-z0-9]+"
    ABBR = "([A-Z]+)[A-Z_]"
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

def getXY(dataset):
    # dataset => A dataset with extracted features

    X = {}
    Y = {}

    for ftype in ["keywords", "hashtags", "urls", "refs", "all"]:
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

def tweet_vector(tweet):
    tv = {}
    for ftype in ["keywords", "hashtags", "urls", "refs", "all"]:
        ids = register(idtable[ftype], tweet[ftype], False)
        n = len(idtable[ftype])
        vector = [0] * n
        for id in ids:
            if id == None: continue # unseen values! <-- do something maybe?
            vector[id] = 1
        tv[ftype] = vector

    return tv

def remove_stopwords(words):
    swords = set([w.strip() for w in open("stopwords.txt").readlines()])
    wset = set(words)
    return list(wset.difference(swords))
    
def get_class(label):
    l = label.strip().lower()
    if l == "sports": return SPORTS
    if l == "politics": return POLITICS

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

training_set = []
data = []
with open(TRAINING) as f:
    for l in f.readlines():
##    data = [l.split(' ', 2) for l in f.readlines() ]
        if l != "\n":
            data.append(l.split(' ', 2))
    for row in data:
        fs = get_features(row[0], row[-1], get_class(row[1]))
        training_set.append(fs)

l = len(training_set)

random.shuffle(training_set)
training_set_75pc = training_set[0:int(l * .75)]
training_set_25pc = training_set[int(l * .75):]

validation_set = []

with open(VALIDATION) as f:
    for line in f.readlines():
        info = line.split(' ', 1)
        fs = get_features(info[0], info[-1])
        validation_set.append(fs)

V_LARGE = 0.80
l = len(validation_set)
validation_set_large = training_set[0:int(l * V_LARGE)]
validation_set_small = training_set[int(l * V_LARGE):]
