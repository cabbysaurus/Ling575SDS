import os
import re
from difflib import SequenceMatcher


# go through each line, check the current system and user utterance vs the prior, add the similarity ration as columns
def add_similarities(input_text):
    return_str = []
    for i, line in enumerate(input_text):
        if i == 0:
            line += '|0.0|0.0'
            continue
        split_line = line.split('|')
        sys_utt = split_line[2]
        user_utt = split_line[4]
        prior_line = input_text[i-1]
        prior_split = prior_line.split('|')
        prior_sys = prior_split[2]
        prior_user = prior_split[4]
        sys_sim = SequenceMatcher(None, sys_utt, prior_sys).ratio()
        user_sim = SequenceMatcher(None, user_utt, prior_user).ratio()
        line = line.replace(' \n', '')
        line += '|' + str(sys_sim) + '|' + str(user_sim)
        return_str.append(line) #+ '\n'

    return return_str


# clean text and return it
def clean_text(input_text):
    return_txt = []
    for line in input_text:
        line = re.sub("[\(\[].*?[\)\]]", "", line).rstrip()
        line = line.replace(' "', '"')
        return_txt.append(line)

    return return_txt


# go through each file, see if there is any repetition. If there is, add the

# go through each file, get a count of the amount of times they were angry or frustrated


def main():
    input_dir = 'speakers/utterances'
    #count = 0
    for dir_file in os.listdir(input_dir):
        input_file = os.path.join(input_dir, dir_file)
        f = open(input_file, 'r')
        #print(str(input_file))
        input_text = f.readlines()
        print (input_text)

        input_text = clean_text(input_text)
        input_text = add_similarities(input_text)
        print (input_text)
        #count += (len(input_text))
    #print(count)

if __name__ == '__main__':
    main()

