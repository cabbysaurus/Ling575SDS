#!/usr/bin/env python

import os
import lxml
import re
import sys
import nltk
import csv

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import defaultdict

class Analyze(object):
    def __init__(self):
        self._tasks = {}

    def add_row(self, row):
        task_id = row[0].rsplit("_", 1)[0]
        if task_id not in self._tasks:
            self._tasks[task_id] = Task(task_id)
        self._tasks[task_id].append(row)

    def summarize(self):
        print "Total: ", len(self._tasks)
        c = self.count_by_system()
        for key, value in c.iteritems():
            print "%5s: %d" % (key, value)

    def count_by_system(self):
        c = defaultdict(int)
        for task_id in self._tasks.iterkeys():
            system = task_id.split("_")[-2]
            c[system] += 1
        return c

class Task(object):
    def __init__(self, task_id):
        self.id = task_id
        self._list = []

    def append(self, row):
        self._list.append(row)

def main(argv=sys.argv):
    filepath = "raw.csv"
    if len(argv) > 1:
        filepath = argv[1]
    a = Analyze()
    with open('raw.csv', 'rb') as csvfile:
        raw_reader = csv.reader(csvfile)
        for row in raw_reader:
            # read the header
            break
        for row in raw_reader:
            a.add_row(row)
    a.summarize()

if __name__ == "__main__":
    main()
