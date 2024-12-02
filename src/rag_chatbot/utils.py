# src/rag_chatbot/utils.py

import logging
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

def setup_logging():
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(
        filename='logs/interactions.log',
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
    )

# def log_interaction(user_query, response, matched=False):
#     timestamp = datetime.datetime.now().isoformat()
#     log_entry = f"{timestamp} - User: {user_query} | Chatbot: {response}"
#     logging.info(log_entry)
#     if not matched:
#         with open('logs/unanswered_queries.log', 'a', encoding='utf-8') as f:
#             f.write(f"{timestamp} - {user_query}\n")

def log_interaction(user_query, response, matched=False):
    timestamp = datetime.datetime.now().isoformat()
    log_data = {
        'timestamp': timestamp,
        'user_query': user_query,
        'response': response,
        'matched': matched
    }
    log_json = json.dumps(log_data)
    
    # Determine the folder based on whether the query was matched
    folder = "unmatched" if not matched else "all"
    log_key = f"logs/interactions/{folder}/{timestamp}.json"
    
    try:
        # Upload the log to S3
        s3.put_object(Bucket=os.getenv("HR_AWS_S3_BUCKET"), Key=log_key, Body=log_json)
        print(f"Log uploaded to S3: {log_key}")
    except Exception as e:
        print(f"Failed to upload log to S3: {e}")


def is_greeting(message):
    GREETINGS = ['hello', 'hi', 'hey', 'greetings']
    return message.strip().lower() in GREETINGS

def is_farewell(message):
    FAREWELLS = ['bye', 'goodbye', 'see you', 'exit', 'quit']
    return message.strip().lower() in FAREWELLS
