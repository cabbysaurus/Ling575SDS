#!/bin/python

import os
import lxml
import re

from lxml import etree
from collections import defaultdict

def output_tags(t, uttid, sentiment_list):
    chunks = uttid.split("_")
    node_id = chunks[0]+chunks[1]
    for tag in sentiment_list:
        users = t.xpath('//comm2000/task[@pin="%s"]//utterance[@speaker="user" and @number="%s"]' % (node_id, tag['id']))
        if len(users) == 1:
            user = users[0]
            texts = {}
            for text in user.findall("text"):
                texts[text.attrib['type']] = text.text
            return "%s|%s|%s|%s|%s" % (uttid, tag.get("id"), tag.get("tag"), str(texts.get("asr")).strip(), str(texts.get("transcription")).strip())
        else:
            pass
            # print node_id, tag
    
def main():
    sentiment_tag_dir = "/corpora/UWCL/communicator-frustration"
    raw_data = "/corpora/LDC/LDC04T15/2000_comm_dialog_act/data/da_tagged_communicator_2000.xml"
    uttid_regex = re.compile("(?P<prefix>[\w\_]+)_usr(?P<usr>\d+) (?P<tag>\w+)")
    for ft in ("consensus-test.txt", "consensus-train.txt"):
        sentiment_filepath = os.path.join(sentiment_tag_dir, ft)
        tags = defaultdict(list)
        with open(sentiment_filepath, "r") as sentiment_f:
            for line in sentiment_f.readlines():
                m = uttid_regex.match(line.strip())
                if m is not None:
                    d = m.groupdict()
                    prefix = d.get('prefix')
                    user_id = d.get('usr')
                    tag = d.get('tag')
                    tags[prefix].append({'id': int(user_id), 'tag': tag}) 
                else:
                    pass
        with open(raw_data, "r") as raw_f:
            filepath = {
                "consensus-test.txt": "test",
                "consensus-train.txt": "train",
            }.get(ft)
            with open(filepath, "w") as out_f:
                t = etree.parse(raw_f)
                for key in tags.iterkeys():
                    out_f.write(output_tags(t, key, tags[key]))
                    out_f.write("\n")

if __name__ == "__main__":
    main()
