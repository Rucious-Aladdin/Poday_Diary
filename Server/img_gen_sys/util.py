# -*- coding: utf-8
import os
import argparse
import requests
import json
import getpass
import copy

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

def get_request_params(args, remove_keys = ["host"]):
    args_dict = vars(copy.deepcopy(args))
    for key in remove_keys:
        if key in args_dict.keys():
            args_dict.pop(key, None)
    return args_dict

def send_generation_request(args):
    try:
        api_key = args.api_key
    except:
        raise ValueError("api_key 가 없거나 잘못되었습니다.")
    headers = {
        "Accept": "image/*",
        "Authorization": f"Bearer {api_key}"
    }
    params = get_request_params(args)
    files = {"none":""}
    response = requests.post(
        str(args.host),
        headers=headers,
        files=files,
        data=params
    )
    if not response.ok:
        raise Exception(f"HTTP {response.status_code}: {response.text}")
    return response