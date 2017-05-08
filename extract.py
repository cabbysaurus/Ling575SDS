#!/bin/python

import os
import lxml
import re
import itertools

from lxml import etree
from collections import defaultdict, OrderedDict

class Processor(object):
    uttid_regex = re.compile("(?P<prefix>[\w\_]+)_usr(?P<usr>\d+) (?P<tag>\w+)")
    FILEPATH_2000 =  "/corpora/LDC/LDC04T15/2000_comm_dialog_act/data/da_tagged_communicator_2000.xml"
    FILEPATH_2001 = "/corpora/LDC/LDC04T16/data/da_tagged_communicator_2001.xml"
    def __init__(self):
        self._file_2000 = open(self.FILEPATH_2000, "r")
        self._file_2001 = open(self.FILEPATH_2001, "r")
        self._t_2000 = etree.parse(self._file_2000)
        self._t_2001 = etree.parse(self._file_2001)

    def get_turn_text(self, turn, text_types=[]):
        ret = OrderedDict() 
        for text in turn.iter("text"):
            ret[text.attrib["type"]] = text.text
        return ret

    def display(self, system, user, task_id, number):
        last_system = None
        if len(system) != 0:
            (key, last_system) = system.popitem(last=True)
        print """%s_%s,"%s","%s","%s" """ % (task_id, number, str(last_system).strip(), str(user.get("asr")).strip(),
                                             str(user.get("transcription")).strip()) 
             
    def output(self):
        print "id,question,response_asr,response_transcription"
        for task in itertools.chain(self._t_2000.iter("task"), self._t_2001.iter("task")):
            system = OrderedDict()
            users = OrderedDict()
            attrib = task.attrib
            system_id = attrib.get("system")
            system_id = {
                "Colorado": "COL",
                "Lucent": "LUC" }.get(system_id, system_id)
            task_id = "_".join([attrib.get("year"), attrib.get("month"), attrib.get("day"), system_id, attrib.get("pin")])
            for turn in task.iter("turn"): 
                if turn.attrib["speaker"] == "system":
                    system = self.get_turn_text(turn)
                elif turn.attrib["speaker"] == "user":
                    users = self.get_turn_text(turn)
                    self.display(system, users, task_id, turn.attrib["number"])
        
                                     
def main():
    p = Processor()
    p.output()

if __name__ == "__main__":
    main()
