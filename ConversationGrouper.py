# creates a separate file for each conversation based on the date and speaker id

def main():
    input_file = "extract.txt"
    input_f = open(input_file, 'r')
    input_text = input_f.readlines()[1:]
    handle_input(input_text)


def handle_input(input_text):
    speaker_utterances = {}
    for line in input_text:
        # first check to make sure it has tags
        split_line = line.split('|')
        if split_line[1] == '' or split_line[1] == ' ':
            continue

        split_line = line.split('_')
        date = str(split_line[0]+split_line[1]+split_line[2])
        speaker_id = split_line[4]
        if date in speaker_utterances:
            if speaker_id in speaker_utterances[date]:
                speaker_utterances[date][speaker_id].append(line)
            else:
                speaker_utterances[date][speaker_id] = []
                speaker_utterances[date][speaker_id].append(line)

        else:
            speaker_utterances[date] = {}
            speaker_utterances[date][speaker_id] = []
            speaker_utterances[date][speaker_id].append(line)

    output_files(speaker_utterances)


def output_files(speaker_utterances):
    output_dir = "speakers/utterances/"
    for date in speaker_utterances:
        for speaker in speaker_utterances[date]:
            output_file = output_dir + date + '_' + speaker + '.txt'
            output_f = open(output_file, 'w')
            for utt in speaker_utterances[date][speaker]:
                output_f.write(utt)

if __name__ == '__main__':
    main()