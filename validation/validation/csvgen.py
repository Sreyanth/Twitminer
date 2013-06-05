import pdb

DATASETS = "datasets"
TRAINING = DATASETS + "/training.txt"
VALIDATION = DATASETS + "/validation.txt"

for dataset in [TRAINING, VALIDATION]:
    lines = open(dataset).read()

    output = []
    lines_list = lines.split('\n')

    for line in lines_list:
        tmp = line.split(' ')
        tmp = tmp[0:2] + [' '.join(tmp[2:])]

        output.append(', '.join(tmp))
        

    open(dataset.replace('txt', 'csv'), 'w').write('\n'.join(output))
