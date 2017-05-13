def main():

    extracted_file = "train"
    n_file = "n_utterances.txt"
    a_file = "a_utterances.txt"
    as_file = "as_utterances.txt"
    af_file = "af_utterances.txt"
    dt_file = "dt_utterances.txt"
    na_file = "na_utterances.txt"
    no_file = "no_utterances.txt"

    n_utterances = []
    a_utterances = []
    as_utterances = []
    af_utterances = []
    dt_utterances = []
    na_utterances = []
    no_utterances = []

    with open(extracted_file, "r") as ef:
        for line in ef.readlines():
            split_line = line.split('|')
            tag = split_line[2].lower()
            utt = "{0}|{1}".format(split_line[3], split_line[4])
            if tag == 'n' or tag == '?':
                n_utterances.append(utt)
            elif tag == 'a':
                a_utterances.append(utt)
            elif tag == 'as':
                as_utterances.append(utt)
            elif tag == 'af':
                af_utterances.append(utt)
            elif tag == 'dt':
                dt_utterances.append(utt)
            elif tag == 'na' or tag == 'naq':
                na_utterances.append(utt)
            else:
                no_utterances.append(utt)

    output(n_file, n_utterances)
    output(a_file, a_utterances)
    output(as_file, as_utterances)
    output(af_file, af_utterances)
    output(dt_file, dt_utterances)
    output(na_file, na_utterances)
    output(no_file, no_utterances)


def output(out_file, utterances):
    with open(out_file, "w") as out:
        for utt in utterances:
            out.write(utt)

if __name__ == "__main__":
    main()
