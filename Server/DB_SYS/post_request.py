# -*- coding: utf-8
import requests
import json

def get_song_info(diary, date, user_id, addr, port):
    url = f"http://{addr}:{port}/recommend/music"
    headers = {'Content-Type': 'application/json'}
    data = {
        "diary": diary,
        "date" : date,
        "user_id": user_id
    }
    response = requests.post(url=url, headers=headers, data=json.dumps(data))
    return response