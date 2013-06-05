# This code will compare the output of both baiyes and decision tree classifier
# Then, if output is same for a tweet, it is considered correct.
# Else, if Compare it with the output of gaussian too, and then decide the
# Dominating class as the label.
# Just to check the accuracy. No 80% shuffling is being made.

RESULTS = "tmp/validation"

BAYES = []
DECISION = []
GAUSSIAN = []
OUTPUT = []

with open(RESULTS+"/bayes.txt", "r+") as guessfile:
    for line in guessfile.readlines():
        BAYES.append(line)

with open(RESULTS+"/decisiontree.txt", "r+") as guessfile:
    for line in guessfile.readlines():
        DECISION.append(line)

with open(RESULTS+"/gaussian.txt", "r+") as guessfile:
    for line in guessfile.readlines():
        GAUSSIAN.append(line)

for i in range(len(BAYES)):
    if BAYES[i] == DECISION[i]:
        line = BAYES[i]
    elif BAYES[i] == GAUSSIAN[i]:
        line = BAYES[i]
    else:
        line = DECISION[i]
    OUTPUT.append(line)

with open(RESULTS+"/best.txt", "w+") as output:
    output.writelines(OUTPUT)
    output.close()