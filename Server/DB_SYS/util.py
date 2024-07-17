# -*- coding: utf-8
import os
import argparse
import json

def load_text_file(path, filename):
    path_to_file = os.path.join(path, filename)
    with open(path_to_file, "r") as f:
        texts = f.read()
    return texts

def load_config(raw_text):
    gpt_config = raw_text.split("\n")
    config_dict = {}
    for config in gpt_config:
        if config.strip():
            config = config.split()
            if len(config) == 2:
                name, value = config[0], config[1]
            else:
                name, value = config[0], " ".join(config[1:])
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

def get_path(user_id):
    config_path = os.path.join("./user_id", user_id)
    text_path = os.path.join(config_path, "data")
    img_path = os.path.join(text_path, "img")
    # Ensure directories exist, create if they don't    
    for path in [config_path, img_path, text_path]:
        if not os.path.exists(path):
            os.makedirs(path)

    return text_path, img_path, config_path

def json2dict(json_file):
    dictionary_file = {}
    
    try:
        with open(json_file, 'r', encoding='utf-8') as file:
            dictionary_file = json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{json_file}' not found.")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON in file '{json_file}'.")
    
    return dictionary_file

def write_text_file(path, dictionary):
    with open(path, "w") as f:
        for k, v in dictionary.items():
            if k != "user_id":
                f.write(str(k) + " " + str(v) + "\n")
