# src/main.py

from chatbot import Chatbot
from utils import log_interaction

def run_chatbot():
    bot = Chatbot()
    print("Welcome to the Highrise FAQ Chatbot!")
    print("Type 'exit' to end the conversation.\n")

    while True:
        user_query = input("You: ")
        if user_query.lower() in ['exit', 'quit', 'bye']:
            print("Chatbot: Goodbye! Feel free to come back if you have more questions.")
            log_interaction(user_query, "Goodbye! Feel free to come back if you have more questions.", matched=True)
            break
        response, matched = bot.get_response(user_query)
        print(f"Chatbot: {response}\n")
        # Log the interaction
        log_interaction(user_query, response, matched)

if __name__ == '__main__':
    run_chatbot()
