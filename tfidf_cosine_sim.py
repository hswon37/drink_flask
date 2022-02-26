#tfidf_cosine_sim.py

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def make_tfidf_cosine_sim(data):
    tfidf_vector = TfidfVectorizer()
    tfidf_matrix = tfidf_vector.fit_transform(data['types'] + ' ' + data['region'] + ' ' + data['maker'] + ' ' + data['ABV'] + ' ' + data['styles']).toarray()
    tfidf_matrix_feature = tfidf_vector.get_feature_names()
    tfidf_matrix = pd.DataFrame(tfidf_matrix, columns=tfidf_matrix_feature, index = data.name)

    cosine_sim = cosine_similarity(tfidf_matrix)
    cosine_sim_df = pd.DataFrame(cosine_sim, index = data.name, columns = data.name)

    return cosine_sim_df