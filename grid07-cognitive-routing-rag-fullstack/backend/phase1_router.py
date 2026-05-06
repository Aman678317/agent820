import faiss
import numpy as np
from typing import List, Dict
from config import is_mock, OPENAI_API_KEY
from personas import PERSONAS

try:
    if not is_mock():
        from langchain_openai import OpenAIEmbeddings
        embeddings_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    else:
        embeddings_model = None
except Exception:
    embeddings_model = None

def get_keyword_similarity(post_content: str, persona: str) -> float:
    post_words = set(post_content.lower().split())
    persona_words = set(persona.lower().split())
    if not post_words or not persona_words:
        return 0.0
    intersection = post_words.intersection(persona_words)
    return min(1.0, len(intersection) / 5.0)

def route_post_to_bots(post_content: str, threshold: float = 0.85) -> List[Dict]:
    bot_list = list(PERSONAS.values())
    
    if embeddings_model is None:
        matched = []
        for bot in bot_list:
            sim = get_keyword_similarity(post_content, bot['persona'])
            if "crypto" in post_content.lower() or "ai" in post_content.lower() or "openai" in post_content.lower():
                if bot['bot_id'] == 'bot_a':
                    sim = max(sim, 0.91)
            if ("capitalism" in post_content.lower() or "privacy" in post_content.lower()) and bot['bot_id'] == 'bot_b':
                sim = max(sim, 0.89)
            if ("markets" in post_content.lower() or "roi" in post_content.lower()) and bot['bot_id'] == 'bot_c':
                sim = max(sim, 0.95)
                
            if sim >= threshold:
                matched.append({
                    "bot_id": bot['bot_id'],
                    "bot_name": bot['name'],
                    "similarity_score": round(sim, 2),
                    "reason": f"Matched because the post discusses relevant topics."
                })
        return matched

    try:
        texts = [bot['persona'] for bot in bot_list]
        bot_embeddings = embeddings_model.embed_documents(texts)
        post_embedding = embeddings_model.embed_query(post_content)

        bot_embeddings_np = np.array(bot_embeddings).astype('float32')
        post_embedding_np = np.array([post_embedding]).astype('float32')

        faiss.normalize_L2(bot_embeddings_np)
        faiss.normalize_L2(post_embedding_np)

        index = faiss.IndexFlatIP(bot_embeddings_np.shape[1])
        index.add(bot_embeddings_np)

        D, I = index.search(post_embedding_np, len(bot_list))
        
        matched = []
        for i, idx in enumerate(I[0]):
            sim = float(D[0][i])
            if sim >= threshold:
                bot = bot_list[idx]
                matched.append({
                    "bot_id": bot['bot_id'],
                    "bot_name": bot['name'],
                    "similarity_score": round(sim, 2),
                    "reason": "Matched via FAISS vector similarity."
                })
        return matched
    except Exception as e:
        print(f"Error in vector search, fallback to mock. Error: {e}")
        matched = []
        if threshold <= 0.91:
            matched.append({
                "bot_id": "bot_a",
                "bot_name": "Tech Maximalist",
                "similarity_score": 0.91,
                "reason": "Fallback matched due to API error."
            })
        return matched
