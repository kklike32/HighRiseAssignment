# src/chatbot.py

import json
import numpy as np
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords

from utils import setup_logging, log_interaction, is_greeting, is_farewell
from synonyms import expand_query

class Chatbot:
    def __init__(self, data_file='data/processed_faq_data.json'):
        self.data_file = data_file
        self.load_data()
        self.setup_nlp_tools()
        self.setup_vectorizer()
        setup_logging()

    def load_data(self):
        with open(self.data_file, 'r', encoding='utf-8') as f:
            self.faq_data = json.load(f)
        self.questions = [entry['processed_question'] for entry in self.faq_data]
        self.answers = [entry['content'] for entry in self.faq_data]

    def setup_nlp_tools(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def setup_vectorizer(self):
        self.vectorizer = TfidfVectorizer()
        self.X = self.vectorizer.fit_transform(self.questions)

    def preprocess_query(self, query):
        # Preprocess the query using the same steps
        query = query.lower()
        query = re.sub(r'[^\w\s]', '', query)
        query = ' '.join(query.split())
        tokens = nltk.word_tokenize(query)
        tokens = [self.lemmatizer.lemmatize(word) for word in tokens if word not in self.stop_words]
        preprocessed_query = ' '.join(tokens)
        return preprocessed_query

    def find_best_match(self, query):
        # Expand query with synonyms
        expanded_query = expand_query(query)
        # Preprocess the expanded query
        processed_query = self.preprocess_query(expanded_query)
        # Vectorize the query
        query_vec = self.vectorizer.transform([processed_query])
        # Compute cosine similarity
        similarities = cosine_similarity(query_vec, self.X)
        # Get the index of the best match
        best_match_idx = np.argmax(similarities)
        # Get the similarity score
        best_score = similarities[0][best_match_idx]
        return best_match_idx, best_score

    def get_response(self, user_query):
        # Check for greetings and farewells
        if is_greeting(user_query):
            return "Hello! How can I assist you today?", True
        if is_farewell(user_query):
            return "Goodbye! Feel free to come back if you have more questions.", True

        best_match_idx, best_score = self.find_best_match(user_query)
        SIMILARITY_THRESHOLD = 0.2  # Adjust based on testing

        if best_score >= SIMILARITY_THRESHOLD:
            answer = self.answers[best_match_idx]
            return answer, True
        else:
            response = "I'm sorry, I couldn't find an answer to your question."
            response += " Please try rephrasing it or check the Highrise FAQ page."
            return response, False
