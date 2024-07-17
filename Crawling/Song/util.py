## util.py - has hard_coded_dictionary
## has preprocess text ... [USR], [BOT] tokens!
import torch
import sys

int2emo = {
    0: "기쁨", 1:"당황", 2:"분노", 3:"불안", 4:"상처", 5:"슬픔", 6:"중립"
}

def preprocess_text(text):
    text = text.split(" [SEP] ")
    result = ""
    for i in range(len(text)):
        if i % 2 == 0:
            if len(result) == 0:
                result += "[USR] " + text[i]
            else:
                result += " [USR] " + text[i]
        else:
            result += " [BOT] " + text[i]
    return result

"""
if __name__ == "__main__":
    text = sys.argv[1]
    print(preprocess_text(text))
    print(int2emo[0])
"""