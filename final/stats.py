#!/usr/bin/env python

"""
#-------------------------------------------------------------------------------
# Name:        stats.py
# Purpose:     To get the statistics on the training_set
#              Based on which we can select most of the
#              SPORTS_FOR_SURE_TAGS and POLITICS_FOR_SURE_TAGS
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
from features import *

SPORTS = 2
POLITICS = 1

stats = {SPORTS: {}, POLITICS: {}}

ftypes = ["all", "keywords", "hashtags", "urls", "refs"] # Feature Types

# keywords  => keywords extracted
# hashtags  => hashtags extracted
# urls      => URLs extracted
# refs      => @refs extracted
# all       => all the above info!!

for ftype in ftypes:
    # Initialing the stats dict for each feature type
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

# A file containing all the stats of the features is now generated.
# Using this, we can determine most of the values for SPORTS_FOR_SURE_TAGS
# and POLITICS_FOR_SURE_TAGS lists in the main test.py