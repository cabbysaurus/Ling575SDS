import nltk
from nltk.collocations import *
from nltk.corpus import stopwords
import os
import re


def main():
    input_dir = "emotions/utterances"
    for dir_file in os.listdir(input_dir):
        input_file = os.path.join(input_dir, dir_file)
        file_name = os.path.splitext(os.path.basename(input_file))[0]
        output_file = "emotions/frequencies/" + file_name + "_freqs.txt"
        get_output_stats(input_file, output_file)


def get_output_stats(input_file, output_file):
    input_text = ''
    #bigrams = []
    #trigrams = []
    #words = []
    #collocations =[]
    with open(input_file, 'r') as in_f:
        utterance_list = []
        asr_list = []
        for line in in_f.readlines():
            split_line = line.split('|')
            asr = split_line[2]
            utterance = split_line[3]
            asr_list.append(asr)
            utterance_list.append(utterance)
            clean_utterance = clean_text(utterance)
            input_text += clean_utterance + ' '

        bigrams = get_freq_bigrams(input_text.lower())
        trigrams = get_freq_trigrams(input_text.lower())
        words = get_freq_words(input_text.lower())
        #collocations = get_collocations(input_text)

    with open(output_file, 'w') as out_f:
        out_f.write('Bigrams:\n')
        out_f.write(str(bigrams[0:10]))
        out_f.write('\n')
        out_f.write('Trigrams:\n')
        out_f.write(str(trigrams[0:10]))
        out_f.write('\n')
        out_f.write('Words:\n')
        out_f.write(str(words))
        out_f.write('\n')
        #out_f.write(str(collocations[0:10]))


def clean_text(text):
    text = text.replace('"', '')
    text = text.replace("'", "")
    #text = re.sub("[\[].*?[\]]", "", text)
    text = re.sub("[/\[].*?[/\]]", "", text)
    text = re.sub("[-+\[\]]+", "", text)
    return text


# method to return the most frequent bigrams
def get_freq_bigrams(text):
    tokens = nltk.word_tokenize(text)
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder = BigramCollocationFinder.from_words(tokens)
    finder.apply_freq_filter(3)
    most_freq_bigrams = finder.nbest(bigram_measures.pmi, 20)
    return most_freq_bigrams


# method to return the most frequent trigrams
def get_freq_trigrams(text):
    tokens = nltk.word_tokenize(text)
    trigram_measures = nltk.collocations.TrigramAssocMeasures()
    finder = TrigramCollocationFinder.from_words(tokens)
    finder.apply_freq_filter(3)
    most_freq_trigrams = finder.nbest(trigram_measures.pmi, 20)
    return most_freq_trigrams


# method to return the most frequent words, excluding stop words
def get_freq_words(text):
    text_list = nltk.word_tokenize(text)
    keep_words = []
    for t in text_list:
        if t not in stopwords.words('english'):
            keep_words.append(t)
    fdist = nltk.FreqDist(keep_words)

    return fdist.most_common(20)


def get_collocations(tokens):
    text = nltk.Text(tokens)
    return text.collocations()


# method to get the number of modal verbs
def count_modals(text):
    modals = ['can', 'could', 'may', 'might', 'must', 'will']
    modal_counts = {}
    tokens = nltk.word_tokenize(text)
    fdist = nltk.FreqDist(tokens)
    for m in modals:
        modal_counts[m] = fdist[m]
    return modal_counts


# method to get the length of the longest utterance
def get_longest_utterance(utterance_list):
    longest_len = max(len(utt) for utt in utterance_list)
    return longest_len


# method to get the average length of utterances
def get_average_utterance_length(utterance_list):
    total_length = 0
    for utt in utterance_list:
        total_length += len(utt)
    average = total_length / len(utterance_list)
    return average


# method to get the count of misrecognized utterances
def get_misrecognition_count(asr_list, utterance_list):
    sent_count = 0
    for i in range(0, len(asr_list)):
        asr = clean_text(asr_list[i]).lower()
        utt = clean_text(utterance_list[i]).lower()
        if asr != utt:
            sent_count += 1
    #sent_percentage = float(sent_count) / len(asr_list)
    return sent_count


#def get_sentiment(text):


if __name__ == '__main__':
    main()