from sentence_transformers import SentenceTransformer
from functools import lru_cache
import faiss
import numpy
import json
import numpy as np


model = SentenceTransformer('stsb-distilbert-base')
index = faiss.IndexFlatL2(768)
precomputed_movie_embs = np.load('data/model/movie_embeddings.npy')
index.add(precomputed_movie_embs)
f = open('data/model/embedding_idx_to_movie_id.json')
embedding_idx_to_id = json.load(f)
embedding_idx_to_id = {
    int(key): value for key, value in embedding_idx_to_id.items()
}


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0: 
        return v
    return v / norm

@lru_cache(maxsize=None)
def get_recommended_movies(searchText, numToReturn):
    search_embedding = model.encode(searchText)
    search_embedding = np.array([normalize(search_embedding)]).reshape((1, 768))
    if numToReturn > 250:
        numToReturn = 250
    _, I = index.search(search_embedding, numToReturn)
    movie_ids = [embedding_idx_to_id[idx] for idx in I[0]]
    return movie_ids
