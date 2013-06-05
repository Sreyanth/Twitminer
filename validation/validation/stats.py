import pdb

from features import *

SPORTS = 2
POLITICS = 1

stats = {SPORTS: {}, POLITICS: {}}

ftypes = ["all", "keywords", "hashtags", "urls", "refs"]
for ftype in ftypes:
    stats[SPORTS][ftype] = {}
    stats[POLITICS][ftype] = {}

def add1(table, key):
    if table.has_key(key): table[key] += 1
    else:
        table[key] = 1
    return table[key]

def register(table, keys):
    return [add1(table, k) for k in keys]

for t in training_set:
    for ftype in ftypes:
        l = t["label"]
        register(stats[l][ftype], t[ftype])

stat_cols = []
header = ""
for ftype in ftypes:
    for label in [SPORTS, POLITICS]:
        header += "%s:%s, count, " % (ftype, label)
        s = stats[label][ftype]
        sortable = zip(s.keys(), s.values())
        s_ = sorted(sortable, lambda x, y: y[1] - x[1])
        keys, values = zip(*s_) # <-- this is cool

        stat_cols.append(keys)
        stat_cols.append(values)


rows = max([len(c) for c in stat_cols])

stat_csv = header + "\n"
for i in range(0, rows):
    for c in stat_cols:
        try:
            stat_csv += str(c[i])
        except:
            pass
        stat_csv += ", "
    stat_csv += "\n"

sfile = open("tmp/training_stats.csv", "w")
sfile.write(stat_csv)
sfile.close()
