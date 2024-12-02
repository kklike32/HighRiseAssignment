# src/rag_chatbot/utils.py

import logging
import os
import datetime

def setup_logging():
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(
        filename='logs/interactions.log',
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
    )

def log_interaction(user_query, response, matched=False):
    timestamp = datetime.datetime.now().isoformat()
    log_entry = f"{timestamp} - User: {user_query} | Chatbot: {response}"
    logging.info(log_entry)
    if not matched:
        with open('logs/unanswered_queries.log', 'a', encoding='utf-8') as f:
            f.write(f"{timestamp} - {user_query}\n")

def is_greeting(message):
    GREETINGS = ['hello', 'hi', 'hey', 'greetings']
    return message.strip().lower() in GREETINGS

def is_farewell(message):
    FAREWELLS = ['bye', 'goodbye', 'see you', 'exit', 'quit']
    return message.strip().lower() in FAREWELLS
