# src/rag_chatbot/chatbot.py

import json
import numpy as np
import openai
import os
import faiss
import re
import sys
import os
from openai import OpenAI

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.rag_chatbot.utils import setup_logging, log_interaction, is_greeting, is_farewell

class Chatbot:
    def __init__(self, data_file='data/rag_processed_faq_data.json', embeddings_file='data/faq_embeddings.npy', index_file='data/faiss_index.index'):
        self.data_file = data_file
        self.embeddings_file = embeddings_file
        self.index_file = index_file
        self.load_data()
        self.load_embeddings()
        self.load_faiss_index()
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        setup_logging()

    def load_data(self):
        with open(self.data_file, 'r', encoding='utf-8') as f:
            self.faq_data = json.load(f)

    def load_embeddings(self):
        self.embeddings = np.load(self.embeddings_file).astype('float32')

    def load_faiss_index(self):
        self.index = faiss.read_index(self.index_file)

    def preprocess_query(self, query):
        # Lowercase
        query = query.lower()
        # Remove punctuation
        query = re.sub(r'[^a-zA-Z0-9\s]', '', query)
        # Remove extra whitespace
        query = ' '.join(query.split())
        return query

    def get_query_embedding(self, query):
        response = self.client.embeddings.create(
            input=query,
            model="text-embedding-ada-002"
        )
        # Extract the embedding from the response object
        embedding = np.array(response.data[0].embedding).astype('float32')
        faiss.normalize_L2(embedding.reshape(1, -1))
        return embedding


    def retrieve_relevant_faqs(self, query_embedding, k=3):
        distances, indices = self.index.search(query_embedding.reshape(1, -1), k)
        relevant_faqs = []
        for idx in indices[0]:
            if idx != -1:
                faq_entry = self.faq_data[idx]
                relevant_faqs.append(faq_entry)
        return relevant_faqs

    def generate_response(self, user_query, relevant_faqs):
        context = "\n\n".join([f"Q: {faq['title']}\nA: {faq['content']}" for faq in relevant_faqs])
        prompt = f"""You are a helpful assistant for Highrise app users.

        Use the context below to answer the user's question. If you don't know the answer, or if the answer is not in the context, say "I'm sorry, I couldn't find an answer to your question." and politely suggest the user check the Highrise FAQ website."""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": f"Context:\n{context}\n\nUser Question:\n{user_query}\n\nAnswer:"}
                ],
                max_tokens=200,
                temperature=0.7,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            answer = response.choices[0].message.content.strip()
            return answer
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm sorry, I'm having trouble generating a response right now."

    def get_response(self, user_query):
        # Check for greetings and farewells
        if is_greeting(user_query):
            return "Hello! How can I assist you today?", True
        if is_farewell(user_query):
            return "Goodbye! Feel free to come back if you have more questions.", True
 
        processed_query = self.preprocess_query(user_query)
        query_embedding = self.get_query_embedding(processed_query)
        relevant_faqs = self.retrieve_relevant_faqs(query_embedding, k=3)

        if relevant_faqs:
            answer = self.generate_response(user_query, relevant_faqs)

            # Determine if the answer indicates that the assistant couldn't find the answer
            if "couldn't find an answer" in answer or "could not find an answer" in answer or "don't know the answer" in answer:
                matched = False
            else:
                matched = True

            return answer, matched
        else:
            response = "I'm sorry, I couldn't find an answer to your question. Please try rephrasing it or check the Highrise FAQ website."
            return response, False        