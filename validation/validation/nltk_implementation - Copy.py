#-------------------------------------------------------------------------------
# Name:        NLTK Classifiers
# Purpose:     To win Twitminer!
#
# Authors:      Sreyantha Chary and Shashi Gowda
#
# Created:     13/03/2013
# Copyright:   (c) Sreyantha Chary & Shashi Gowda 2013
# Licence:     Open for non-commercial use! :P
#-------------------------------------------------------------------------------

import nltk
import re
from stemmer import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

DATASETS = "datasets"
TRAINING = DATASETS + "/training.txt"
VALIDATION = DATASETS + "/validation.txt"

HASHTAGS = re.compile("\#([^\s\,\.\#\"\'\+\=\|\$\%\^\:]+)")
URLS1 = re.compile("https?\:\/\/([^\s]+)")
URLS2 = re.compile("www\.([^\s]+)")
REFS = re.compile("\@([^\s\,\.\#\"\'\+\=\|\$\%\^\:\-]+)")
KEYWORDS = re.compile("(\w+)")
WHITESPACE = re.compile("[\s\.\,\'\"\[\]\{\}\;\:\/\&\=\+\-\)\(\*\&\^\%\$\`\|\?\!]+")
STEMMER = PorterStemmer()

def remove_stopwords(words):
    swords = set([w.strip() for w in open("stopwords.txt").readlines()])
    wset = set(words)
    return list(wset.difference(swords))

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
    extended = extended
    return extended

def getpos(string):
    value =''
    result = pos_tag(word_tokenize(string))
    for word, pos in result:
        value = value + word + pos + " "
    return value.strip()

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

def get_words_in_tweets(tweets):
    all_words = []
    for (words, sentiment) in tweets:
        all_words.extend(words)
    return all_words

def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    word_features = wordlist.keys()
    return word_features

def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in tweet_words)
    return features

training_set = []

with open(TRAINING) as f:
    data = [l.split(' ', 2) for l in f.readlines()]
    for row in data:
        fs = get_features(row[0], row[-1], row[1])
        training_set.append(fs)
    f.close()

tweets = []

for tweet_info in training_set:
    words_filtered = [getpos(e.lower()) for e in tweet_info["keywords"] if len(e) >= 2]
    tweets.append((words_filtered, tweet_info["label"]))

word_features = get_word_features(get_words_in_tweets(tweets))

print "Extracting and Applying features!"
training = nltk.classify.apply_features(extract_features, tweets)

print "Training the Classfier!"
classifier = nltk.NaiveBayesClassifier.train(training)

print "Preparing the Validation Set!"
validation_set = []

with open(VALIDATION) as f:
    for line in f.readlines():
        info = line.split(' ', 1)
        fs = get_features(info[0], info[-1])
        validation_set.append(fs)
    f.close()

validation = []

for i in validation_set:
    tweet = " ".join(i["keywords"])
    validation.append((i["id"], tweet.strip()))

results = []

print "Classification started!"
for tweet_info in validation:
    result = "%s %s\n" %(tweet_info[0], classifier.classify(extract_features(getpos(tweet_info[1]).split())))
    #print result, tweet_info[1]
    results.append(result)

with open("tmp/validation/results_nltk.txt", "w+") as OUTPUT:
    OUTPUT.writelines(results)
    OUTPUT.close()

