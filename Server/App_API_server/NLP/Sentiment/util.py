## util.py - has hard_coded_dictionary
## has preprocess text ... [USR], [BOT] tokens!
import torch
import sys

int2emo = {
    0: "기쁨", 1:"당황", 2:"분노", 3:"불안", 4:"상처", 5:"슬픔", 6:"중립"
}

def preprocess_text(text):
    text = text.split("[SEP] ")
    result = ""
    new_texts = []
    for i in range(len(text)):
        if len(text[i]) == 0 or text[i] == " ":
            continue
        else:
            new_texts.append(text[i])
    for i in range(len(new_texts)):
        if i % 2 == 0:
            result += "[USR] " + new_texts[i]
        else:
            result += "[BOT] " + new_texts[i]
    print(result)
    return result