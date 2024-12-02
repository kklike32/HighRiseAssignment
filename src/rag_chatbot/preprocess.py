# src/rag_chatbot/preprocess.py

import json
import re
import nltk
import os
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from tqdm import tqdm

def preprocess_text(text):
    # Initialize lemmatizer and stopwords
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))

    # Lowercase
    text = text.lower()
    # Remove URLs and emails
    text = re.sub(r'\S+@\S+', '', text)
    text = re.sub(r'http\S+', '', text)
    # Remove punctuation and special characters
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    # Tokenize
    tokens = nltk.word_tokenize(text)
    # Remove stopwords and lemmatize
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    # Join tokens back into string
    preprocessed_text = ' '.join(tokens)
    return preprocessed_text

def split_article_into_qa_pairs(entry):
    # Check if the article contains multiple Q&As
    content = entry.get('content', '')
    # Regex pattern to find Q&A pairs
    qa_pattern = r'(Q:.*?(?=Q:|$))'
    matches = re.findall(qa_pattern, content, re.DOTALL)
    
    qa_entries = []
    if matches:
        for qa in matches:
            # Split into question and answer
            qa_split = re.split(r'A:', qa)
            if len(qa_split) == 2:
                question = qa_split[0].strip()
                answer = qa_split[1].strip()
                if question.startswith('Q:'):
                    question = question[2:].strip()
                qa_entries.append({
                    'question': question,
                    'answer': answer,
                    'category': entry.get('category', ''),
                    'url': entry.get('url', ''),
                    'last_updated': entry.get('last_updated', '')
                })
    else:
        # Return the original entry if no Q&A pairs are found
        qa_entries.append({
            'question': entry.get('title', ''),
            'answer': content,
            'category': entry.get('category', ''),
            'url': entry.get('url', ''),
            'last_updated': entry.get('last_updated', '')
        })
    return qa_entries

def split_long_answer(answer, max_words=200):
    sentences = nltk.sent_tokenize(answer)
    chunks = []
    current_chunk = ''
    current_length = 0

    for sentence in sentences:
        sentence_length = len(sentence.split())
        if current_length + sentence_length <= max_words:
            current_chunk += ' ' + sentence
            current_length += sentence_length
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence
            current_length = sentence_length

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

import matplotlib.pyplot as plt

def analyze_word_counts(processed_data):
    word_counts = [len(entry['content'].split()) for entry in processed_data]
    plt.hist(word_counts, bins=50)
    plt.title('Word Count Distribution')
    plt.xlabel('Word Count')
    plt.ylabel('Number of Entries')
    plt.show()

import random

def inspect_sample_entries(processed_data, sample_size=5):
    samples = random.sample(processed_data, sample_size)
    for entry in samples:
        print(f"ID: {entry['id']}")
        print(f"Title: {entry['title']}")
        print(f"Content: {entry['content'][:500]}")  # Print first 500 characters
        print(f"Word Count: {len(entry['content'].split())}")
        print("-" * 50)
        
def check_for_duplicates(processed_data):
    seen_contents = set()
    duplicates = []
    for entry in processed_data:
        content = entry['content']
        if content in seen_contents:
            duplicates.append(entry)
        else:
            seen_contents.add(content)
    print(f"Found {len(duplicates)} duplicate entries.")
    print("Sample duplicates:")
    for entry in duplicates:
        print(f"ID: {entry['id']}")
        print(f"Title: {entry['title']}")
        print(f"Content: {entry['content'][:500]}")


def preprocess_data(input_file='data/faq_data.json', output_file='data/rag_processed_faq_data.json'):
    # Load data from JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        faq_data = json.load(f)

    processed_data = []
    id_counter = 0
    for entry in tqdm(faq_data, desc="Preprocessing data"):
        qa_entries = split_article_into_qa_pairs(entry)
        for qa_entry in qa_entries:
            question = qa_entry['question']
            answer = qa_entry['answer']
            
            # Calculate word count
            word_count = len(answer.split())
            
            # Skip entries with low word count
            if word_count < 20:
                continue  # Skip this entry
            
            # Split long answers into chunks
            if word_count > 300:  # Adjust threshold as needed
                answer_chunks = split_long_answer(answer, max_words=200)
            else:
                answer_chunks = [answer]
            
            for chunk in answer_chunks:
                processed_entry = {
                    'id': id_counter,
                    'title': question,
                    'url': qa_entry['url'],
                    'category': qa_entry['category'],
                    'content': chunk,
                    'last_updated': qa_entry['last_updated'],
                    'text_for_embedding': preprocess_text(chunk)
                }
                processed_data.append(processed_entry)
                id_counter += 1

    # Save processed data to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_data, f, ensure_ascii=False, indent=4)

    print(f"Preprocessed data saved to {output_file}")
    
    analyze_word_counts(processed_data)
    inspect_sample_entries(processed_data)
    # check_for_duplicates(processed_data)

if __name__ == '__main__':
    preprocess_data()