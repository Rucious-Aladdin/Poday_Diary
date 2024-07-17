# -*- coding: utf-8
import os
import json
from error_handler import ErrorHandler
from util import *

class RegisterSystem(ErrorHandler):
    def __init__(self, data):
        self.user_id = data["user_id"]
        self.gender = data["gender"]
        self.age = data["age"]
        self.data = data
        self.default_path = None
        self.init_user_path()

    @classmethod
    def verify_user_data(cls, json_data):
        data = json.loads(json_data)
        return cls(data)

    def init_user_path(self):
        config_filename = "user_config.txt"
        default_path = "./user_id/"
        default_path = os.path.join(default_path, self.user_id)
        self.default_path = default_path
        if not os.path.exists(os.path.join(default_path, config_filename)):
            os.makedirs(os.path.join(default_path, "data/img"))
            self.create_config_file(config_filename)
            self.user_create = True
        else:
            self.user_already_exist_error()

    def create_config_file(self, config_filename):
        write_text_file(os.path.join(self.default_path, config_filename), self.data)
    
    def get_create_flag(self):
        return self.user_create