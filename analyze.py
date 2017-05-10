#!/usr/bin/env python

import os
import lxml
import re
import sys
import nltk
import csv


from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import defaultdict
from difflib import SequenceMatcher

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
        heading = ["REPE"]
        print "  SYS  TOTAL",
        for head in heading:
            print "%12s" % (head),
        print ""
        for system in sorted(self._systems, key=self._systems.get, reverse=True):
            total = self._systems[system]
            print "%5s: %5d" % (system, total),
            for att in heading:
                count = {
                    "REPE": self._repeated_by_system
                }.get(att)(system)
                print "%5d (%.2f)" % (count, float(count)/float(total)),
            print ""

    def _repeated_by_system(self, system):
        count = 0
        for task in filter(lambda t: t.system == system, self._tasks.itervalues()):
            if task._have_repeated:
                count += 1
        return count

    def count_by_system(self):
        c = defaultdict(int)
        for task_id in self._tasks.iterkeys():
            system = task_id.split("_")[-2]
            c[system] += 1
        return c

    def analyze(self):
        self._systems = defaultdict(int)
        for task in self._tasks.itervalues():
            self._systems[task.system] += 1
            task.analyze()

class Sentence(object):
    def __init__(self, row):
        self.id = row[0]
        self.system = row[1]
        self.asr = row[2]
        self.transcribed = row[3]

class Task(object):
    def __init__(self, task_id):
        self.id = task_id
        self._sentences = []
        self.system = task_id.split("_")[-2]
            # attributes
        self._have_repeated = False

    def append(self, row):
        self._sentences.append(Sentence(row))

    def _similarity(self, s1, s2):
        s = SequenceMatcher(lambda x: x==" ", s1, s2)
        return s.ratio()

    def _analyze_repeated_questions(self):
        """Analyze for repeated questions."""
        for i in range(1, len(self._sentences)):
            score = self._similarity(self._sentences[i-1].system,
                                     self._sentences[i].system)
            if score >= 0.9:
                self._have_repeated = True
                break

    def analyze(self):
        self._analyze_repeated_questions()

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
    a.analyze()
    a.summarize()

if __name__ == "__main__":
    main()
