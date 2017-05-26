def main():

    extracted_file = "extract.txt"
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
        input = ef.read()
        lines = input.split("\n")
        for i in range(1, len(lines)-1):
            split_line = lines[i].split('|')
            tag = split_line[1].lower()
            utt = "{0}|{1}|{2}|{3}".format(split_line[1], split_line[2], split_line[3], split_line[4])
            if tag == '' or tag == ' ':
                continue
            elif tag == 'n' or tag == '?':
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
    full_out = "emotions/utterances/" + out_file
    with open(full_out, "w") as out:
        for utt in utterances:
            out.write(utt + '\n')

if __name__ == "__main__":
    main()
