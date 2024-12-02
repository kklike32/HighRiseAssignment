# app.py

import streamlit as st
import sys
import os
import datetime
import json
import boto3

# Initialize S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("HR_AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("HR_AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("HR_AWS_DEFAULT_REGION")
)

# Ensure the project root is in PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from rag_chatbot.chatbot import Chatbot
from rag_chatbot.utils import log_interaction

def log_feedback(user_query, response, feedback):
    timestamp = datetime.datetime.now().isoformat()
    feedback_data = {
        'timestamp': timestamp,
        'user_query': user_query,
        'response': response,
        'feedback': feedback
    }
    feedback_key = f"logs/feedback/{timestamp}.json"
    try:
        s3.put_object(Bucket=os.getenv("HR_AWS_S3_BUCKET"), Key=feedback_key, Body=json.dumps(feedback_data))
        print(f"Feedback uploaded to S3: {feedback_key}")
    except Exception as e:
        print(f"Failed to upload feedback to S3: {e}")


# Initialize the chatbot
bot = Chatbot()

# Initialize session state for conversation history and feedback
if 'conversation' not in st.session_state:
    st.session_state.conversation = []
if 'feedback' not in st.session_state:
    st.session_state.feedback = []
if 'user_input' not in st.session_state:
    st.session_state.user_input = ''  # Initialize input state

def send_message():
    user_query = st.session_state.user_input
    if user_query:
        if user_query.lower() in ['exit', 'quit', 'bye']:
            response = "Goodbye! Feel free to come back if you have more questions."
            matched = True
        else:
            response, matched = bot.get_response(user_query)
        # Append to conversation history
        st.session_state.conversation.append({'user': user_query, 'bot': response})
        # Clear the input box after sending
        st.session_state.user_input = ''  # Clear input
        # Log the interaction
        log_interaction(user_query, response, matched)

st.title("Highrise FAQ Chatbot")

# Display the conversation history
for idx, entry in enumerate(st.session_state.conversation):
    st.markdown(f"**You:** {entry['user']}")
    st.markdown(f"**Chatbot:** {entry['bot']}")
    # Display feedback buttons for each bot response
    if 'feedback' not in entry:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👍", key=f"thumbs_up_{idx}"):
                # st.session_state.conversation[idx]['feedback'] = 'Helpful'
                # # Log feedback
                # timestamp = datetime.datetime.now().isoformat()
                # with open('logs/feedback.log', 'a') as f:
                #     f.write(f"{timestamp} - User: {entry['user']} | Chatbot: {entry['bot']} | Feedback: Helpful\n")
                st.session_state.conversation[idx]['feedback'] = 'Helpful'
                log_feedback(entry['user'], entry['bot'], 'Helpful')
        with col2:
            if st.button("👎", key=f"thumbs_down_{idx}"):
                # st.session_state.conversation[idx]['feedback'] = 'Unhelpful'
                # # Log feedback
                # timestamp = datetime.datetime.now().isoformat()
                # with open('logs/feedback.log', 'a') as f:
                #     f.write(f"{timestamp} - User: {entry['user']} | Chatbot: {entry['bot']} | Feedback: Unhelpful\n")
                st.session_state.conversation[idx]['feedback'] = 'Unhelpful'
                log_feedback(entry['user'], entry['bot'], 'Unhelpful')
    else:
        st.markdown(f"Feedback recorded: {entry['feedback']}")

# Display a text input for the user's question
st.text_input("Type your message here:", key='user_input')

# Use a "Send" button to submit the message with on_click callback
st.button("Send", on_click=send_message)
