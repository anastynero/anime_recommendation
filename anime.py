import pandas as pd
import numpy as np
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel

def text_cleaning(text):
    text = re.sub(r'&quot;', '', text)
    text = re.sub(r'.hack//', '', text)
    text = re.sub(r'&#039;', '', text)
    text = re.sub(r'A&#039;s', '', text)
    text = re.sub(r'I&#039;', 'I\'', text)
    text = re.sub(r'&amp;', 'and', text)
    return text

def give_rec(title):
    anime_data=pd.read_csv('anime.csv')
    anime_data['name'] = anime_data['name'].apply(text_cleaning)
    anime_data['genre'] = anime_data['genre'].fillna('')
    genres_str = anime_data['genre'].str.split(',').astype(str)
    tfv = TfidfVectorizer(min_df=3, max_features=None, strip_accents='unicode', 
                          analyzer='word', token_pattern=r'\w{1,}', ngram_range=(1, 3), 
                          stop_words='english')
    tfv_matrix = tfv.fit_transform(genres_str)
    sig = sigmoid_kernel(tfv_matrix, tfv_matrix)
    indices = pd.Series(anime_data.index, index=anime_data['name']).drop_duplicates()
    idx = indices[title]
    sig_scores = list(enumerate(sig[idx]))
    sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)
    sig_scores = sig_scores[1:11]
    anime_indices = [i[0] for i in sig_scores]
    top_10_similar_anime = anime_data['name'].iloc[anime_indices].values
    return top_10_similar_anime


