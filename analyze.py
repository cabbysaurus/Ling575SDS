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
    TEMPLATE = "%11s"
    def __init__(self):
        self._tasks = {}
        self.sid = SentimentIntensityAnalyzer()

    def add_row(self, row):
        task_id = row['id'].rsplit("_", 1)[0]
        if task_id not in self._tasks:
            self._tasks[task_id] = Task(task_id)
        self._tasks[task_id].append(row)

    def summarize(self):
        func_map = {
            "REPE": self._repeated_by_system,
            "REPE2": self._repeated_by_system_two,
            "SIGH": self._sigh_by_system,
            "ASR":  self._asr_by_system,
            "SENT_COMP": self._sentiment_by_system,
            "SENT_POS": self._pos_by_system,
            "SENT_NEG": self._neg_by_system,
            "TURNS": self._turns_by_system,
            "LEN_SYS": self._system_len_by_system,
            "LEN_USR": self._usr_len_by_system,
        }
        print "Total: ", len(self._tasks)
        heading = sorted(func_map.iterkeys())
        print "  SYS  TOTAL",
        for head in heading:
            print self.TEMPLATE % (head),
        print ""
        for year in ("2000", "2001"):
            print "Year: %s" % (year)
            for system in sorted(self._systems, key=self._systems.get, reverse=True):
                total = self._systems[system][year]
                print "%5s: %5d" % (system, total),
                for att in heading:
                    func = func_map.get(att)
                    out = func(system, total, year=year)
                    print self.TEMPLATE % (out),
                print ""

    def _repeated_by_system(self, system, total, year=None):
        count = self._by_system(system, "_have_repeated", year=year)
        if total == 0 and count == 0:
            return ""
        return "%5d(%.2f)" % (count, float(count)/float(total))

    def _repeated_by_system_two(self, system, total, year=None):
        count = self._by_system(system, "_have_repeated_two", year=year)
        if total == 0 and count == 0:
            return ""
        return "%5d(%.2f)" % (count, float(count)/float(total))

    def _sigh_by_system(self, system, total, year=None):
        count = self._by_system(system, "_have_sigh", year=year)
        if total == 0 and count == 0:
            return ""
        return "%5d (%.2f)" % (count, float(count)/float(total))

    def _by_system(self, system, key, year=None):
        count = 0
        for task in filter(lambda t: t.system == system and t.year == year,
                           self._tasks.itervalues()):
            if getattr(task, key):
                count += 1
        return count

    def _value_by_system(self, system, key, year=None):
        s = []
        for task in filter(lambda t: t.system == system and t.year == year,
                           self._tasks.itervalues()):
            s.append(getattr(task, key))
        return s

    def _asr_by_system(self, system, count, year=None):
        s = self._value_by_system(system, "_asr_score", year=year)
        if count == 0 and len(s) == 0:
            return ""
        ret = sum(s)/float(len(s))
        return self.TEMPLATE % ("%.2f" % ret)

    def _system_len_by_system(self, system, count, year=None):
        s = self._value_by_system(system, "_system_len", year=year)
        if count == 0 and len(s) == 0:
            return ""
        ret = sum(s)/float(len(s))
        return self.TEMPLATE % ("%.1f" % ret)

    def _usr_len_by_system(self, system, count, year=None):
        s = self._value_by_system(system, "_usr_len", year=year)
        if count == 0 and len(s) == 0:
            return ""
        ret = sum(s)/float(len(s))
        return self.TEMPLATE % ("%.1f" % ret)

    def _sentiment_by_system(self, system, count, year=None):
        s = self._value_by_system(system, "_compound", year=year)
        if count == 0 and len(s) == 0:
            return ""
        ret = sum(s)/float(len(s))
        return self.TEMPLATE % ("%.2f" % ret)

    def _pos_by_system(self, system, count, year=None):
        s = self._value_by_system(system, "_pos", year=year)
        if count == 0 and len(s) == 0:
            return ""
        ret = sum(s)/float(len(s))
        return self.TEMPLATE % ("%.2f" % ret)

    def _neg_by_system(self, system, count, year=None):
        s = self._value_by_system(system, "_neg", year=year)
        if count == 0 and len(s) == 0:
            return ""
        ret = sum(s)/float(len(s))
        return self.TEMPLATE % ("%.2f" % ret)

    def _turns_by_system(self, system, count, year=None):
        """Calculate the average number of turns by system"""
        s = self._value_by_system(system, "_turns", year=year)
        if count == 0 and len(s) == 0:
            return ""
        ret = sum(s)/float(len(s))
        return self.TEMPLATE % ("%d" % ret)

    def analyze(self):
        self._systems = defaultdict(lambda: defaultdict(int))
        for task in self._tasks.itervalues():
            self._systems[task.system][task.year] += 1
            task.analyze(self)

class Sentence(object):
    def __init__(self, row):
        self.id = row['id']
        self.system = row['question']
        self.asr = row['response_asr']
        self.transcribed = row['response_transcription']
        self.filtered = []
        self._compound = 0.0
        self.transcribed_tokens = []
        (self.transcribed_tokens, self.filtered) = self.filter_bracket(word_tokenize(self.transcribed))
        self.transcribed_sanitized = " ".join(self.transcribed_tokens)
        self.system_tokens = word_tokenize(self.system)
        self._system_len = len(self.system_tokens)
        self._usr_len = len(self.transcribed_tokens)
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
        task_id_chunks = task_id.split("_")
        self.system = task_id_chunks[-2]
        self.year = task_id_chunks[0]
            # attributes
        self._have_repeated = False
        self._have_repeated_two = False
        self._have_sigh = False
        self._compound = 0.0
        self._asr_score = 0.0
        self._turns = 0

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
            if score >= 0.95:
                self._have_repeated = True
                if i >= 2:
                    score_2 = self._similarity(self._sentences[i-2].system,
                                             self._sentences[i].system)
                    if score_2 >= 0.95:
                        self._have_repeated_two = True
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

        d = {
            '_compound': [],
            '_neg': [],
            '_pos': [],
        }
        for s in self._sentences:
            ss = parent.sid.polarity_scores(s.transcribed_sanitized)
            s._compound = ss.get('compound')
            for key in ('compound', 'pos', 'neg'):
                v = ss.get(key)
                k = "_" + key
                setattr(s, k, v)
                d[k].append(v)
        for k in d.iterkeys():
            if len(d[k]) > 0:
                setattr(self, k, sum(d[k])/float(len(d[k])))
            else:
                setattr(self, k, 0.0)

    def analyze(self, parent):
        self._turns = len(self._sentences)
        self._system_len = sum([s._system_len for s in self._sentences])/self._turns
        self._usr_len = sum([s._usr_len for s in self._sentences])/self._turns
        self._analyze_repeated_questions()
        self._analyze_sentiment(parent)
        self._analyze_asr()


def main(argv=sys.argv):
    filepath = "raw.csv"
    if len(argv) > 1:
        filepath = argv[1]
    a = Analyze()
    with open('raw.csv', 'rb') as csvfile:
        raw_reader = csv.DictReader(csvfile)
        for row in raw_reader:
            a.add_row(row)
    a.analyze()
    a.summarize()

if __name__ == "__main__":
    main()
