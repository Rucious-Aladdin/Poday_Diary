
import requests
import json
from post_request import *
import base64
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

if __name__ == "__main__":

    url = "http://127.0.0.1:5003/db/init"
    headers = {"Content-Type": "application/json"}
    data = {"user_id": "hwal"}

    response = requests.post(url, headers=headers, json=data)

    url = "http://127.0.0.1:5003/db/read_row"
    headers = {"Content-Type" : "application/json"}
    data = {"date": "2022-01-01"}

    response = requests.post(url, headers=headers, json=data)

    #print(response.status_code)
    #print(json.loads(response.content)["response"].keys())
    #print(json.loads(response.content)["response"]["song_indices"])
    #print(type(json.loads(response.content)["response"]["song_indices"]))


    print(json.loads(response.content)["response"]["songs"].keys())
    #print(json.loads(response.content)["response"]["songs"])
    print(type(json.loads(response.content)["response"]["songs"]))
    songs = json.loads(response.content)["response"]["songs"]
    for k, v in songs.items():
        if k != "images":
            print(v)
        else:
            # base64 문자열이 있음(jpg format). list 내에.
            # 사진 보여주는거 작성해줘. 
            for i, img_str in enumerate(v):
                img_data = base64.b64decode(img_str)
                img = Image.open(BytesIO(img_data))

                # 이미지를 matplotlib을 사용하여 표시
                plt.figure()
                plt.imshow(img)
                plt.axis('off')  # 축을 숨김
                plt.title(f"Image {i+1}")
                plt.show()