#!/bin/python

import os
import lxml
import re

from lxml import etree
from collections import defaultdict

class Processor(object):
    uttid_regex = re.compile("(?P<prefix>[\w\_]+)_usr(?P<usr>\d+) (?P<tag>\w+)")
    FILEPATH_2000 =  "/corpora/LDC/LDC04T15/2000_comm_dialog_act/data/da_tagged_communicator_2000.xml"
    FILEPATH_2001 = "/corpora/LDC/LDC04T16/data/da_tagged_communicator_2001.xml"
    def __init__(self):
        self._file_2000 = open(self.FILEPATH_2000, "r")
        #self._file_2001 = open(self.FILEPATH_2001, "r")
        self._t_2000 = etree.parse(self._file_2000)
        #self._t_2001 = etree.parse(self._file_2001)

    def output_tags(self, tags):
        for key in tags.iterkeys():
            if "2000" in key:
                chunks = key.split("_")
                node_id = chunks[0]+chunks[1]
                for tag in tags[key]:
                    users = self._t_2000.xpath('//comm2000/task[@pin="%s"]//utterance[@speaker="user" and @number="%s"]' % (node_id, tag['id']))
                    if len(users) == 1:
                        user = users[0]
                        texts = {}
                        for text in user.findall("text"):
                            texts[text.attrib['type']] = text.text
                        yield "%s|%s|%s|%s|%s" % (key, tag.get("id"), tag.get("tag"), str(texts.get("asr")).strip(), str(texts.get("transcription")).strip())
    
def main():
    sentiment_tag_dir = "/corpora/UWCL/communicator-frustration"
    p = Processor()
    for ft in ("consensus-test.txt", "consensus-train.txt"):
        sentiment_filepath = os.path.join(sentiment_tag_dir, ft)
        tags = defaultdict(list)
        with open(sentiment_filepath, "r") as sentiment_f:
            for line in sentiment_f.readlines():
                m = p.uttid_regex.match(line.strip())
                if m is not None:
                    d = m.groupdict()
                    prefix = d.get('prefix')
                    user_id = d.get('usr')
                    tag = d.get('tag')
                    tags[prefix].append({'id': int(user_id), 'tag': tag}) 
                else:
                    pass
        filepath = {
            "consensus-test.txt": "test",
            "consensus-train.txt": "train",
        }.get(ft)
        with open(filepath, "w") as out_f:
            for line in p.output_tags(tags):
                out_f.write(line)
                out_f.write("\n")

if __name__ == "__main__":
    main()
