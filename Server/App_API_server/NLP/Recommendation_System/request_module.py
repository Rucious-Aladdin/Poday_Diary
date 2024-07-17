# -*- coding: utf-8
import requests
import json

class RequestHandler:
    def __init__(self):
        pass

    def get_vector_req(self, req_dict):
        url = f"http://{self.args.host_ipaddr}:{self.args.sentiment_port}/sentiment/predict"
        headers = {'Content-Type': 'application/json'}
        data = req_dict
        response = requests.post(url=url, headers=headers, data=json.dumps(data))
        return response
    
    def update_db_req(self):
        user_id = self.args.user_id
        date = self.args.date

        # DB_INIT_REQUEST
        url = f"http://{self.args.host_ipaddr}:{self.args.db_port}/db/init"
        headers = {'Content-Type': 'application/json'}
        data = {
            "user_id": user_id
        }
        _ = requests.post(url=url, headers=headers, data=json.dumps(data))

        #DB_UPDATE_REQUEST
        url = f"http://{self.args.host_ipaddr}:{self.args.db_port}/db/create_update"
        headers = {'Content-Type': 'application/json'}
        if self.args.media_type == "music":
            type_req = "song_indices"
        else:
            type_req = "book_indices"
        data = {
            "date": date,
            str(type_req): self.top_k_indices
        }

        response = requests.post(url=url, headers=headers, data=json.dumps(data))
        return response
    