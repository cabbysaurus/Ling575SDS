#!/bin/python

import os
import lxml
import re
import sys
import nltk

from nltk.sentiment.vader import SentimentIntensityAnalyzer

def main(argv=sys.argv):
    filepath = "test"
    if len(argv) > 1:
        filepath = argv[1]
    sid = SentimentIntensityAnalyzer()
    with open(filepath, "r") as f:
        for line in f.readlines():
            chunks = line.strip().split("|")
            asr = chunks[-2]
            transcribed = chunks[-1]
            ss = sid.polarity_scores(asr)
            print asr
            for k in sorted(ss):
                print '{0}: {1}, '.format(k, ss[k]),
            print ""
    
if __name__ == "__main__":
    main()
