answers = []
correct = 0
wrong = 0
total = 0

def getlabel(string):
    if string == "s":
        return "Sports"
    else:
        return "Politics"

with open("CustomizedBayes_info.txt", "r+") as f:
    for line in f.readlines():
        split = line.split(' ', 2)
        answer = raw_input(split[2])
        if getlabel(answer) == split[1]:
            correct += 1
        else:
            wrong+=1
        total+=1
        answers.append(answer)
        print "Correct - %d\t\t Wrong - %d\t\t Total - %d" % (correct, wrong, total)
    f.close()
        
