# -*- coding: utf-8
from util import *
import pandas as pd
from error_handler import ErrorHandler
import json
import datetime
import numpy as np
import shutil

class DataBaseSystem(ErrorHandler):
    def __init__(self, text_path, image_path, config_path, user_id, max_recommend_num):
        super().__init__()
        self.args = load_config(load_text_file(config_path, "user_config.txt"))
        self.text_path, self.image_path = text_path, image_path
        self.user_id = user_id
        self.user_create = False
        self.user_df = self.load_data_frame()
        self.max_recommend_num = max_recommend_num

    @classmethod
    def load_user_database(cls, user_id, max_recommend_num=8):
        text_path, image_path, config_path = get_path(user_id)
        return cls(text_path, image_path, config_path, user_id, max_recommend_num)

    def get_columns(self):
        return self.user_df.columns.to_list()

    def set_initial_arguments(self):
        return
    
    def create_row(self, json_data):
        result = json.loads(json_data)
        date = result["date"]
        self.last_date = date
        if self.find_target_row(date):
            for col in self.get_columns():
                if col in result.keys():
                    k = col; v = result[k]
                    processed_value = self.preprocess(k, v)
                    if k == "song_indices" or k == "book_indices":
                        self.user_df.loc[self.user_df["date"] == date, k] = processed_value
                    elif k != "date":
                        self.user_df.loc[self.user_df["date"] == date, k] = processed_value
            self.row_create = False
        else:
            new_row = pd.DataFrame(columns=self.get_columns())
            for col in self.get_columns():
                if col in result:
                    processed_value = self.preprocess(col, result[col])
                    new_row.loc[0, col] = processed_value
                else:
                    if col == "emotion": # default value as "neutral"
                        new_row.loc[0, col] = 6
                    else:
                        new_row.loc[0, col] = None
            self.user_df = pd.concat([self.user_df, new_row], ignore_index=True, axis=0)
            self.row_create = True
        
        self.save_image()
        self.save_df()

    def save_df(self):
        self.user_df.to_csv(os.path.join(self.text_path, self.filename), index=False, sep="\t")

    def save_image(self): ## last_image.jpg 파일을 저장
        image_path = f"~/img_gen_sys/img/{self.user_id}-{self.last_date}.jpg"
        image_path = os.path.expanduser(image_path)
        if os.path.exists(image_path):
            self.saved_image_name = f"{self.user_id}-{self.last_date}.jpg"
            self.user_df.loc[self.user_df["date"]==self.last_date, "img_filename"] = self.saved_image_name
            destination = f"./user_id/{self.user_id}/data/img/{self.saved_image_name}"
            shutil.move(image_path, destination)
        else:
            self.saved_image_name = None
        
    def preprocess(self, k, v):
        if k == "emotion":
            return int(v)
        elif k == "song_indices" or k == "book_indices":
            if "str" in str(type(v)):
                v = json.loads(v)
            indicies_list = v
            indicies_list = [str(x) for x in indicies_list]
            return "/".join(indicies_list)
        else:
            return v
        

    def find_target_row(self, date, display=False):
        self.target_row = self.user_df[self.user_df["date"] == date]
        if self.target_row.shape[0] == 1:
            if display:
                print(self.target_row)
            return True
        else:
            if display:
                print("해당하는 행이 존재하지 않습니다.")
            return False
    
    def delete_row(self, json_data):
        self.found_row = True
        data = json.loads(json_data)
        date = data["date"]
        if not self.find_target_row(date):
            self.target_row_not_found_error(date)
        self.user_df = self.user_df[self.user_df["date"] != date]
        self.save_df()
        return self.found_row, date
    
    def init_df(self):
        return

    def get_df(self):
        return self.user_df
    
    def load_data_frame(self, filename="data.csv"):
        self.filename = filename
        try:
            return pd.read_csv(os.path.join(self.text_path, self.filename), encoding="utf-8", sep="\t")
        except FileNotFoundError:
            return self.handle_df_not_found_error(self.filename)
    
