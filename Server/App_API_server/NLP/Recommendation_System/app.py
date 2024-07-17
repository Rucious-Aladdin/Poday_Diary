# -*- coding: utf-8
from flask import make_response ,request, Flask
from util import *
from recommend_module import RecommendationSystem
import base64

app = Flask(__name__)
host_addr = "0.0.0.0"
host_port = 5004

#### Music Recommendation
base_path = "./music/"
matrix_path = "./music/song_vectors_matrix.pkl"
df_path = "./music/songs_with_images.csv"
song_module = RecommendationSystem.load_matrix_and_dictionary_file(
        media_type = "music", 
        matrix_path=matrix_path, 
        df_path=df_path,
        user_id="dummy",
        date="dummy"
)

# diary, date, user_id
@app.route("/recommend/music", methods=["POST"])
def recommend_songs():
    data = request.json
    diary = data["diary"]; date = data["date"]; user_id = data["user_id"]
    print("diary: ", diary)
    print("date: ", date)
    print("user_id: ", user_id)
    song_module.args.date = date; song_module.args.user_id = user_id
    print(song_module.get_similarity_topk_index(diary))
    return song_module.make_responses()

#### Book Recommendation
"""
base_path = "./book/"
matrix_path = "./book/book_vectors_matrix.pkl"
df_path = "./book/books_with_images.csv"
song_module = RecommendationSystem.load_matrix_and_dictionary_file(
        media_type = "book", 
        matrix_path=matrix_path, 
        df_path=df_path,
        user_id="dummy",
        date="dummy"
)
"""

"""
@app.route("/recommend/book", methods=["POST"])
def recommend_songs():
    data = request.json
    diary = data["diary"]; date = data["date"]; user_id = data["user_id"]
    song_module.args.date = date; song_module.args.user_id = user_id
    print(song_module.get_similarity_topk_index(diary))
    return song_module.make_responses()
"""

if __name__ == "__main__":
    app.run(
        host=host_addr,
        port=host_port,
        debug=True
    )