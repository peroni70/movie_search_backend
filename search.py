from sentence_transformers import SentenceTransformer
from functools import lru_cache
from sklearn.preprocessing import normalize
import faiss
import numpy
import json
import numpy as np


model = SentenceTransformer('stsb-distilbert-base')
index = faiss.IndexFlatIP(768)
precomputed_movie_embs = np.load('data/model/movie_embeddings.npy')
index.add(precomputed_movie_embs)
f = open('data/model/embedding_idx_to_movie_id.json')
embedding_idx_to_id = json.load(f)
embedding_idx_to_id = {
    int(key): value for key, value in embedding_idx_to_id.items()
}

@lru_cache(maxsize=None)
def get_recommended_movies(searchText, numToReturn):
    search_embedding = model.encode(searchText)
    search_embedding = normalize(search_embedding.reshape(1,-1), norm='l2')
    if numToReturn > 250:
        numToReturn = 250
    _, I = index.search(search_embedding, numToReturn)
    movie_ids = [embedding_idx_to_id[idx] for idx in I[0]]
    return movie_ids
