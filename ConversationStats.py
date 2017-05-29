import os
import re
from difflib import SequenceMatcher

#system_repetition = {}
#user_repetition = {}
#system_recognition = {}

# go through each line, check the current system and user utterance vs the prior, add the similarity ration as columns
def add_similarities(input_text):
    return_str = []
    for i, line in enumerate(input_text):
        if i == 0:
            line += '|0.0|0.0'
            continue
        split_line = line.split('|')
        sys_utt = split_line[2]
        sys_heard = split_line[3]
        user_utt = split_line[4]
        prior_line = input_text[i-1]
        prior_split = prior_line.split('|')
        prior_sys = prior_split[2]
        prior_user = prior_split[4]
        sys_sim = SequenceMatcher(None, sys_utt, prior_sys).ratio()
        user_sim = SequenceMatcher(None, user_utt, prior_user).ratio()
        utt_sim = SequenceMatcher(None, sys_heard, user_utt).ratio()
        line = line.replace(' \n', '')
        line += '|' + str(sys_sim) + '|' + str(user_sim) + '|' + str(utt_sim)
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


# go through each file, see if there is any repetition. If there is, look at the emotion and add to the count
def check_system_repetition(input_text):
    system_repetition = {}
    for line in input_text:
        split_line = line.split('|')
        sys_sim = split_line[5]
        emotion = split_line[1]

        if sys_sim > 0.9:
            if emotion in system_repetition:
                system_repetition[emotion] += 1
            else:
                system_repetition[emotion] = 1

    return system_repetition


def check_user_repetition(input_text):
    user_repetition = {}
    for line in input_text:
        split_line = line.split('|')
        user_sim = split_line[6]
        emotion = split_line[1]

        if user_sim > 0.9:
            if emotion in user_repetition:
                user_repetition[emotion] += 1
            else:
                user_repetition[emotion] = 1

    return user_repetition


# go through each file and look for emotions when what the system heard was different than what the user said
def check_sys_recognition(input_text):
    system_recognition = {}
    #system_recognition = {}
    for line in input_text:
        split_line = line.split('|')
        sys_rec = split_line[7]
        emotion = split_line[1]
        if sys_rec != 1.0:
            if emotion in system_recognition:
                system_recognition[emotion] += 1
            else:
                system_recognition[emotion] = 1

    return system_recognition


# count how many files have angry or angry/frustrated
def check_has_angry(input_text):
    for line in input_text:
        split_line = line.split('|')
        emotion = split_line[1]
        if emotion == 'a' or emotion == 'af':
            return True
    return False


# go through each file, get a count of the amount of times they were angry or frustrated to get a sense of
# saturation per conversation
def get_angry_count(input_text):
    count = 0
    for line in input_text:
        split_line = line.split('|')
        emotion = split_line[1]
        if emotion == 'a' or emotion == 'af':
            count += 1
    return count


# get a count of the number of conversations in which there was an angry streak (i.e. 3 or more a/af utts in a row)
def check_angry_streak(input_text):
    streak_count = 0
    for i in range(0, len(input_text)):
        line = input_text[i]
        split_line = line.split('|')
        emotion = split_line[1]
        if streak_count >= 5:
            return True
        if emotion == 'a' or emotion == 'af':
            streak_count += 1
        else:
            streak_count = 0

    return False


def main():
    input_dir = 'speakers/utterances'
    #system_recognition = {}
    #system_repetition = {}
    user_repetition = {}
    has_angry_frustrated = 0
    angry_count = 0
    angry_counts = {}
    streak_count = 0

    for dir_file in os.listdir(input_dir):
        input_file = os.path.join(input_dir, dir_file)
        f = open(input_file, 'r')
        input_text = f.readlines()

        if check_has_angry(input_text):
            has_angry_frustrated += 1
            count = get_angry_count(input_text)
            angry_count += count
            if count in angry_counts:
                angry_counts[count] += 1
            else:
                angry_counts[count] = 1

            if check_angry_streak(input_text):
                streak_count += 1

        input_text = clean_text(input_text)
        input_text = add_similarities(input_text)
        #sys_rep = check_system_repetition(input_text)
        user_rep = check_user_repetition(input_text)
        #sys_rec = check_sys_recognition(input_text)

        # go through each item in the returned dict and add it to the overall one
        # for emotion in sys_rec:
        #     if emotion in system_recognition:
        #         system_recognition[emotion] += sys_rec[emotion]
        #     else:
        #         system_recognition[emotion] = sys_rec[emotion]
        #
        # for emotion in sys_rep:
        #     if emotion in system_repetition:
        #         system_repetition[emotion] += sys_rep[emotion]
        #     else:
        #         system_repetition[emotion] = sys_rep[emotion]

        for emotion in user_rep:
            if emotion in user_repetition:
                user_repetition[emotion] += user_rep[emotion]
            else:
                user_repetition[emotion] = user_rep[emotion]

    print str(has_angry_frustrated)
    print str(angry_count)
    print str(angry_counts)
    print str(streak_count)
    # no need to print them all because they are all the same which does make sense...
    #print "System Repetition: " + str(system_repetition) + '\n'
    print "User Repetition: " + str(user_repetition) + '\n'
    #print "System Recognition: " + str(system_recognition)


if __name__ == '__main__':
    main()

