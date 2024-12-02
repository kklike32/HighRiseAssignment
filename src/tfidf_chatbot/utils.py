# src/tfidf_chatbot/utils.py

import logging
import os

# Configure logging
def setup_logging():
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(
        filename='logs/interactions.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )

def log_interaction(user_query, response, matched=False):
    if matched:
        logging.info(f"User Query: {user_query}")
        logging.info(f"Chatbot Response: {response}")
    else:
        logging.info(f"User Query: {user_query}")
        logging.info("Chatbot Response: No suitable answer found.")
        # Log unanswered or misclassified questions
        with open('logs/unanswered_queries.log', 'a', encoding='utf-8') as f:
            f.write(f"{user_query}\n")

def is_greeting(message):
    GREETINGS = ['hello', 'hi', 'hey', 'greetings']
    return message.lower() in GREETINGS

def is_farewell(message):
    FAREWELLS = ['bye', 'goodbye', 'see you', 'exit', 'quit']
    return message.lower() in FAREWELLS
