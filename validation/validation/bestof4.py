# This code will compare the output of 4 - Bayes, NLTK Bayes, Gaussian and SGD
# Then, if output is same for a tweet, it is considered correct.
# Else, if Compare it with the output of gaussian too, and then decide the
# Dominating class as the label.
# Just to check the accuracy. No 80% shuffling is being made.

RESULTS = "tmp/validation"

NLTK = []
BAYES = []
SGD = []
GAUSSIAN = []
OUTPUT = []

with open(RESULTS+"/bayes.txt", "r+") as guessfile:
    for line in guessfile.readlines():
        BAYES.append(line)
    guessfile.close()

with open(RESULTS+"/sgd.txt", "r+") as guessfile:
    for line in guessfile.readlines():
        SGD.append(line)
    guessfile.close()
    
with open(RESULTS+"/gaussian.txt", "r+") as guessfile:
    for line in guessfile.readlines():
        GAUSSIAN.append(line)
    guessfile.close()
    
with open(RESULTS+"/results_nltk.txt", "r+") as guessfile:
    for line in guessfile.readlines():
        NLTK.append(line)
    guessfile.close()

for i in range(len(BAYES)):
    poss = []
    poss.append(BAYES[i])
    poss.append(NLTK[i])
    poss.append(GAUSSIAN[i])
    poss.append(SGD[i])

    options = set(poss)
    if len(options) == 1:
        for i in options:
            option = i
        OUTPUT.append(option)
    else:
        option1, option2 = options
        if poss.count(option1) >= poss.count(option2):
            OUTPUT.append(option1)
        else:
            OUTPUT.append(option2)
    
with open(RESULTS+"/best.txt", "w+") as output:
    output.writelines(OUTPUT)
    output.close()
