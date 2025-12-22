from sklearn.metrics.pairwise import cosine_similarity
from embeddings_manager import post_embeddings, get_embedding_safe

def find_similar_post(query):
    query_embeddings = get_embedding_safe(query)
    best_score, best_post = 0, None

    for post_item in post_embeddings:
        for query_chunk in query_embeddings:
            for post_chunk in post_item["embeddings"]:
                score = cosine_similarity([query_chunk], [post_chunk])[0][0]
                if score > best_score:
                    best_score = score
                    best_post = post_item["post"]
    return best_post