import nltk
import os
import re
import operator


def get_pos_tags(in_file):
    tagged_lines = []
    with open(in_file, "r") as in_f:
        for line in in_f.readlines():
            split_line = line.split("|")
            utterance = split_line[3].lower()
            clean_utt = clean_text(utterance)
            if clean_utt == '' or clean_utt == ' ':
                continue
            tokens = nltk.word_tokenize(clean_utt)
            pos_tag = nltk.pos_tag(tokens)
            tagged_lines.append(pos_tag)
    return tagged_lines


def clean_text(text):
    #text = text.replace("'s", " is")
    #text = text.replace("nt", ' not')
    #text = text.replace("'ll,", ' will')
    #print(text)
    text = re.sub("[/\[].*?[/\]]", "", text)
    #text = re.sub("[^0-9a-zA-Z ]+", "", text)
    text = re.sub("[-+\[\]]+", "", text)
    text = text.replace('"', '')
    #text = text.replace("'", "")
    #print(text)
    return text


def get_freq_tags(tagged_lines):
    tagged_counts = {}
    for line in tagged_lines:
        for tup in line:
            tag = str(tup[1])
            if tag in tagged_counts:
                tagged_counts[tag] += 1
            else:
                tagged_counts[tag] = 1
    tagged_counts = sorted(tagged_counts.items(), key=operator.itemgetter(1))
    return tagged_counts


def main():
    input_dir = "emotions/utterances"
    for dir_file in os.listdir(input_dir):
        input_file = os.path.join(input_dir, dir_file)
        file_name = os.path.splitext(os.path.basename(input_file))[0]
        out_file = "emotions/tags/" + file_name + "_tagged.txt"
        out_freqs = "emotions/frequencies/" + file_name + "_tag_frequencies.txt"
        tagged_lines = get_pos_tags(input_file)

        with open(out_file, "w") as out_f:
            for line in tagged_lines:
                out_f.write(str(line))
                out_f.write("\n")

        sorted_tagged_counts = get_freq_tags(tagged_lines)
        with open(out_freqs, 'w') as out_f:
            out_f.write(str(sorted_tagged_counts))

if __name__ == '__main__':
    main()
