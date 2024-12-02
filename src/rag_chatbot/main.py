# src/rag_chatbot/main.py

import sys
import os

# Add the project root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.rag_chatbot.chatbot import Chatbot
from src.rag_chatbot.utils import log_interaction

def run_chatbot():
    bot = Chatbot()
    print("Welcome to the Highrise FAQ Chatbot!")
    print("Type 'exit' to end the conversation.\n")

    while True:
        user_query = input("You: ")
        if user_query.lower() in ['exit', 'quit', 'bye']:
            response = "Goodbye! Feel free to come back if you have more questions."
            print(f"Chatbot: {response}\n")
            log_interaction(user_query, response, matched=True)
            break
        response, matched = bot.get_response(user_query)
        print(f"Chatbot: {response}\n")
        # Log the interaction
        log_interaction(user_query, response, matched)

if __name__ == '__main__':
    run_chatbot()
