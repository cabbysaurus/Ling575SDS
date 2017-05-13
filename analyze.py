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
from nltk import word_tokenize

class Analyze(object):
    def __init__(self):
        self._tasks = {}
        self.sid = SentimentIntensityAnalyzer()

    def add_row(self, row):
        task_id = row[0].rsplit("_", 1)[0]
        if task_id not in self._tasks:
            self._tasks[task_id] = Task(task_id)
        self._tasks[task_id].append(row)

    def summarize(self):
        print "Total: ", len(self._tasks)
        heading = ["REPE", "SIGH", "SENT", "ASR"]
        print "  SYS  TOTAL",
        for head in heading:
            print "%12s" % (head),
        print ""
        for system in sorted(self._systems, key=self._systems.get, reverse=True):
            total = self._systems[system]
            print "%5s: %5d" % (system, total),
            for att in heading:
                out = {
                    "REPE": self._repeated_by_system,
                    "SIGH": self._sigh_by_system,
                    "ASR":  self._asr_by_system,
                    "SENT": self._sentiment_by_system,
                }.get(att)(system, total)
                print "%12s" % (out),
            print ""

    def _repeated_by_system(self, system, total):
        count = self._by_system(system, "_have_repeated")
        return "%5d (%.2f)" % (count, float(count)/float(total))

    def _sigh_by_system(self, system, total):
        count = self._by_system(system, "_have_sigh")
        return "%5d (%.2f)" % (count, float(count)/float(total))

    def _by_system(self, system, key):
        count = 0
        for task in filter(lambda t: t.system == system, self._tasks.itervalues()):
            if getattr(task, key):
                count += 1
        return count

    def _value_by_system(self, system, key):
        s = []
        for task in filter(lambda t: t.system == system, self._tasks.itervalues()):
            s.append(getattr(task, key))
        return s

    def _asr_by_system(self, system, count):
        s = self._value_by_system(system, "_asr_score")
        ret = sum(s)/float(len(s))
        return "%12s" % ("%.2f" % ret)

    def _sentiment_by_system(self, system, count):
        s = self._value_by_system(system, "_compound")
        ret = sum(s)/float(len(s))
        return "%12s" % ("%.2f" % ret)

    def analyze(self):
        self._systems = defaultdict(int)
        for task in self._tasks.itervalues():
            self._systems[task.system] += 1
            task.analyze(self)

class Sentence(object):
    def __init__(self, row):
        self.id = row[0]
        self.system = row[1]
        self.asr = row[2]
        self.transcribed = row[3]
        self.filtered = []
        self._compound = 0.0
        self.transcribed_tokens = []
        (self.transcribed_tokens, self.filtered) = self.filter_bracket(word_tokenize(self.transcribed))
        self.transcribed_sanitized = " ".join(self.transcribed_tokens)
        # print self.id, self.filtered, self.transcribed_sanitized

    def filter_bracket(self, tokens):
        ret = []
        filtered = []
        bracket = 0
        for t in tokens:
            if t == ']': bracket -= 1
            elif t == '[': bracket += 1
            if bracket > 0 or t == ']':
                if t not in ["[", "]"]:
                    filtered.append(t)
                continue
            ret.append(t)
        return (ret, filtered)

class Task(object):
    def __init__(self, task_id):
        self.id = task_id
        self._sentences = []
        self.system = task_id.split("_")[-2]
            # attributes
        self._have_repeated = False
        self._have_sigh = False
        self._compound = 0.0
        self._asr_score = 0.0

    def append(self, row):
        self._sentences.append(Sentence(row))

    def _similarity(self, s1, s2):
        s = SequenceMatcher(lambda x: x==" ", s1, s2)
        return s.ratio()

    def _analyze_repeated_questions(self):
        """Analyze for repeated questions. If similarity score > 0.9 then true."""
        for i in range(1, len(self._sentences)):
            score = self._similarity(self._sentences[i-1].system,
                                     self._sentences[i].system)
            if score >= 0.9:
                self._have_repeated = True
                break

    def _analyze_asr(self):
        """Compare the similarity of the transcribed_sanitized, and asr."""
        scores = []
        for i in range(len(self._sentences)):
            score = self._similarity(self._sentences[i].transcribed_sanitized.lower(),
                                     self._sentences[i].asr.lower())
            scores.append(score)
        self._asr_score = sum(scores)/float(len(scores))

    def _analyze_sentiment(self, parent):
        """Look for [sigh] in the transcribed text. Calculate the "compound" sentiment
           in the transcribed_sanitized text"""
        for s in self._sentences:
            if 'sigh' in s.filtered:
                self._have_sigh = True
                break
        c = []
        for s in self._sentences:
            ss = parent.sid.polarity_scores(s.transcribed_sanitized)
            s._compound = ss.get('compound')
            if s._compound != 0.0:
                c.append(s._compound)
        if len(c) > 0:
            self._compound = sum(c)/float(len(c))
        else:
            self._compound = 0.0

    def analyze(self, parent):
        self._analyze_repeated_questions()
        self._analyze_sentiment(parent)
        self._analyze_asr()

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
