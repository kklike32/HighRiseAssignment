# src/rag_chatbot/compute_embeddings.py

import json
import numpy as np
import openai
import os
from tqdm import tqdm

def compute_embeddings(data_file='data/rag_processed_faq_data.json', embeddings_file='data/faq_embeddings.npy'):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    if not openai.api_key:
        raise ValueError("Please set your OpenAI API key as an environment variable 'OPENAI_API_KEY'.")

    # Load preprocessed data
    with open(data_file, 'r', encoding='utf-8') as f:
        faq_data = json.load(f)

    # Collect texts to embed
    texts = [entry['text_for_embedding'] for entry in faq_data]

    # Compute embeddings
    embeddings = []
    for text in tqdm(texts, desc='Computing embeddings'):
        try:
            response = openai.embeddings.create(
                input=text,
                model="text-embedding-ada-002"
            )
            embedding = response.data[0].embedding
            embeddings.append(embedding)
        except Exception as e:
            print(f"Error computing embedding for text: {text[:30]}... Error: {e}")
            embeddings.append([0]*1536)  # Embedding size of 1536

    # Save embeddings
    embeddings = np.array(embeddings, dtype='float32')
    np.save(embeddings_file, embeddings)
    print(f"Embeddings saved to {embeddings_file}")

if __name__ == '__main__':
    compute_embeddings()
