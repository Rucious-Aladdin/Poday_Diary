# -*- coding: utf-8
import sklearn
import pandas as pd
import numpy as np
from request_module import RequestHandler
from types import SimpleNamespace
from util import *
import json
from sklearn.neighbors import NearestNeighbors
import os

class RecommendationSystem(RequestHandler):
    def __init__(self, args):
        self.args = args
        self.matrix = load_pickle(self.args.matrix_path)
        self.idx2title = load_pickle(os.path.join(self.args.base_path, "index2title.pkl"))
        self.idx2artist = load_pickle(os.path.join(self.args.base_path, "index2artist.pkl"))
        self.idx2images = load_pickle(os.path.join(self.args.base_path, "index2base64images.pkl"))

    @classmethod
    def load_matrix_and_dictionary_file(cls, media_type, matrix_path, df_path, user_id, date):
        args = SimpleNamespace()
        args.matrix_path = matrix_path
        args.df_path = df_path
        args.media_type = media_type
        args.base_path = f"./{media_type}/"
        args.user_id = user_id
        args.date = date
        args.host_ipaddr = "141.223.140.4"
        args.sentiment_port = 5000
        args.db_port = 5003
        return cls(args)

    def make_responses(self):
        response = {}
        if self.args.media_type == "music":
            if len(self.top_k_indices) == 0:
                response["messages"] = "Error has Occured. No Song has been founded."
            else:
                response["messages"] = "Working Normally!"
        elif self.args.media_type == "book":
            if len(self.top_k_indices) == 0:
                response["messages"] = "Error has Occured. No Book has been founded."
            else:
                response["messages"] = "Working Normally!"

        if len(self.top_k_indices) == 0:
            response["images"] = []
            response["status"] = "false"
            response["titles"] = []
            response["artists"] = []
            response["indices"] = []
        else:
            response["images"] = [self.idx2images[idx] for idx in self.top_k_indices]
            response["status"] = "true"
            response["indices"] = [idx for idx in self.top_k_indices]
            response["titles"] = [self.idx2title[idx] for idx in self.top_k_indices]
            response["artists"] = [self.idx2artist[idx] for idx in self.top_k_indices]
        self.update_db_req()
        return json.dumps(response, ensure_ascii=False) 

    # cosine similarity
    def get_similarity_topk_index(self, diary, top_k=3):
        self.diary = diary
        source_vector = self.get_media_vector()
        cosine_similarities = self.cosine_similarity_all(source_vector)
        self.top_k_indices = np.argsort(cosine_similarities)[-top_k:][::-1].tolist()
        return self.top_k_indices

    ## knn measure
    def get_knn_topk_index(self, diary, top_k=3):
        self.diary = diary
        source_vector = self.get_media_vector().reshape(1, -1)  # Reshape for compatibility with sklearn
        nbrs = NearestNeighbors(n_neighbors=top_k, algorithm='auto', metric='euclidean').fit(self.matrix)
        _ , self.top_k_indices = nbrs.kneighbors(source_vector)
        self.top_k_indices = self.top_k_indices[0].tolist()
        return self.top_k_indices

    ## correlation
    def get_pearson_topk_index(self, diary, top_k=3):
        self.diary = diary
        source_vector = self.get_media_vector()
        similarities = []
        
        for target_vector in self.matrix:
            similarity = self.pearson_correlation(source_vector, target_vector)
            similarities.append(similarity)
        
        similarities = np.array(similarities)
        top_k_indices = np.argsort(similarities)[-top_k:][::-1].tolist()
        self.top_k_indices = top_k_indices
        
        return self.top_k_indices
    
    def pearson_correlation(self, v1, v2):
        v1_mean = np.mean(v1)
        v2_mean = np.mean(v2)
        numerator = np.sum((v1 - v1_mean) * (v2 - v2_mean))
        denominator = np.sqrt(np.sum((v1 - v1_mean) ** 2) * np.sum((v2 - v2_mean) ** 2))
        return numerator / denominator

    def get_media_vector(self):
        response = self.get_vector_req({"conversation": "[USR] " + self.diary})
        vector = json.loads(response.content)["context_vector"]
        vector = np.array([float(x) for x in vector])
        return vector
    
    def cosine_similarity_all(self, source_vector):
        dot_product = np.dot(self.matrix, source_vector)
        magnitude_source = np.sqrt(np.sum(source_vector ** 2))
        magnitude_targets = np.sqrt(np.sum(self.matrix ** 2, axis=1))
        cosine_similarities = dot_product / (magnitude_source * magnitude_targets)
        return cosine_similarities

