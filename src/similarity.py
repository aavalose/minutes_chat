import numpy as np
from config import client

def cosine_similarity(v1, v2):
    dot_product = np.dot(v1, v2)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    return dot_product / (norm1 * norm2)

def search_relevant_chunks(chunks, query):
    query_response = client.embeddings.create(
        input=query,
        model="text-embedding-ada-002"
    )
    query_embedding = query_response.data[0].embedding
    
    chunk_similarities = []
    for chunk in chunks:
        response = client.embeddings.create(
            input=chunk,
            model="text-embedding-ada-002"
        )
        similarity = cosine_similarity(query_embedding, response.data[0].embedding)
        chunk_similarities.append((chunk, similarity))
    
    chunk_similarities.sort(key=lambda x: x[1], reverse=True)
    relevant_chunks = [chunk for chunk, similarity in chunk_similarities if similarity > 0.5]
    return relevant_chunks[:5]