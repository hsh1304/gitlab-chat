from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re
from pdf_loader import load_pdf_text_chunks

class Retriever:
    def __init__(self, pdf_path: str, chunk_size=200, overlap=50, top_k=3):
        self.chunks = load_pdf_text_chunks(pdf_path, chunk_size, overlap)
        self.top_k = top_k
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=1000,
            lowercase=True,
            strip_accents='unicode'
        )
        if len(self.chunks) == 0:
            self.tfidf_matrix = None
        else:
            texts = [c["text"] for c in self.chunks]
            self.tfidf_matrix = self.vectorizer.fit_transform(texts)
            print(f"Loaded {len(self.chunks)} chunks from knowledge base")

    def retrieve(self, query: str, top_k: int = None):
        if top_k is None:
            top_k = self.top_k
        if self.tfidf_matrix is None:
            return []
        
        query_clean = re.sub(r'[^\w\s]', ' ', query.lower()).strip()
        
        q_vec = self.vectorizer.transform([query_clean])
        scores = cosine_similarity(q_vec, self.tfidf_matrix)[0]
        
        min_similarity = 0.05
        valid_indices = np.where(scores >= min_similarity)[0]
        
        if len(valid_indices) == 0:
            return []
        
        valid_scores = scores[valid_indices]
        sorted_indices = valid_indices[np.argsort(valid_scores)[::-1]]
        
        results = []
        for i, idx in enumerate(sorted_indices[:top_k]):
            score = float(scores[idx])
            text = self.chunks[idx]["text"]
            
            if len(text) > 500:
                text = text[:500] + "..."
            
            results.append({
                "score": score, 
                "text": text,
                "rank": i + 1
            })
        
        return results
