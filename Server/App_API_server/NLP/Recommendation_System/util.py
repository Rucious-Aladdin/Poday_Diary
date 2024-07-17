# -*- coding: utf-8
import pickle
import numpy as np

int2emo = {
    0: "기쁨", 1:"당황", 2:"분노", 3:"불안", 4:"상처", 5:"슬픔", 6:"중립"
}

def save_pickle(obj, filename):
    with open(filename, 'wb') as file:
        pickle.dump(obj, file)

def load_pickle(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

def cosine_sim(source_vector, target_vector):
    dot_product = np.sum(source_vector * target_vector)
    magnitude_source = np.sqrt(np.sum(source_vector ** 2))
    magnitude_target = np.sqrt(np.sum(target_vector ** 2))
    cosine_similarity = dot_product / (magnitude_source * magnitude_target)
    return cosine_similarity

if __name__ == "__main__":
    a = [1, 1]
    b = [1, 1]
    a = np.array(a)
    b = np.array(b)
    print(cosine_sim(a, b))