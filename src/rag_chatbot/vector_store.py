# src/rag_chatbot/vector_store.py

import faiss
import numpy as np

def build_faiss_index(embeddings_file='data/faq_embeddings.npy', index_file='data/faiss_index.index'):
    # Load embeddings
    embeddings = np.load(embeddings_file)
    embeddings = embeddings.astype('float32')  # FAISS requires float32

    # Build index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)  # Inner Product (cosine similarity)
    faiss.normalize_L2(embeddings)  # Normalize embeddings
    index.add(embeddings)

    # Save index
    faiss.write_index(index, index_file)
    print(f"FAISS index saved to {index_file}")

if __name__ == '__main__':
    build_faiss_index()
