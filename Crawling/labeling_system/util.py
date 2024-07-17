# -*- coding: utf-8
import sounddevice as sd
import wavio
import speech_recognition as sr
from gtts import gTTS
from IPython.display import Audio, display
from mutagen.mp3 import MP3
import time
import openai
from openai import OpenAI
import os
import argparse

def load_text_file(path, filename):
    path_to_file = os.path.join(path, filename)
    with open(path_to_file, "r") as f:
        prompts = f.read()
    return prompts

def load_config(raw_text):
    gpt_config = raw_text.split("\n")
    config_dict = {}
    for config in gpt_config:
        if config.strip():
            config = config.split()
            name, value = config[0], config[1]
            config_dict["--" + name] = value
    parser = argparse.ArgumentParser()
    for name in config_dict.keys():
        parser.add_argument(name)
    
    arg_list = []
    for k, v in config_dict.items():
        arg_list.append(k)
        arg_list.append(str(v))
    
    args = parser.parse_args(arg_list)
    return args