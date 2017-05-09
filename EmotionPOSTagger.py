import nltk
import os
import re


def create_output_tags(in_file, out_file):
    tagged_lines = []
    with open(in_file, "r") as in_f:
        for line in in_f.readlines():
            split_line = line.split("|")
            utterance = split_line[1]
            clean_utt = re.sub("[\[].*?[\]]", "", utterance)
            tokens = nltk.word_tokenize(clean_utt)
            tagged_lines.append(nltk.pos_tag(tokens))

    with open(out_file, "w") as out_f:
        for line in tagged_lines:
            out_f.write(str(line))
            out_f.write("\n")


def main():
    input_dir = "emotions/utterances"
    for dir_file in os.listdir(input_dir):
        input_file = os.path.join(input_dir, dir_file)
        file_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = "emotions/tags/" + file_name + "_tagged.txt"
        create_output_tags(input_file, output_file)

if __name__ == '__main__':
    main()
