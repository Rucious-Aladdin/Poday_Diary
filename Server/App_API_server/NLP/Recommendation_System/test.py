# -*- coding: utf-8
from util import *
import pandas as pd
import os
from recommend_module import RecommendationSystem

def cosine_similarity(source_vector, target_vectors):
    dot_product = np.dot(target_vectors, source_vector)
    magnitude_source = np.sqrt(np.sum(source_vector ** 2))
    magnitude_targets = np.sqrt(np.sum(target_vectors ** 2, axis=1))
    cosine_similarities = dot_product / (magnitude_source * magnitude_targets)
    return cosine_similarities

if __name__ == "__main__":
    base_path = "./music/"
    matrix_path = "./music/song_vectors_matrix.pkl"
    df_path = "./music/songs_with_images.csv"
    df = pd.read_csv(df_path, sep=",")
    print(df.columns)
    print(df.head())
    module = RecommendationSystem.load_matrix_and_dictionary_file(
        media_type = "music", 
        matrix_path=matrix_path, 
        df_path=df_path,
        user_id="hwal",
        date="2024-7-7"
    )
    diary = "오늘은 조용히 있고싶어.. 평온하게.."
    matched_index = module.get_similarity_topk_index(diary, top_k=1)
    song_title = []; index2title=load_pickle("./music/index2artist.pkl")
    for x in matched_index:
        song_title.append(index2title[x])
    print(song_title)
    response = module.make_responses()
    print(response)



"""
    

    matched_index = module.get_pearson_topk_index(diary, top_k=10)
    song_title = []
    for x in matched_index:
        song_title.append(index2title[x])
    print(song_title)

"""