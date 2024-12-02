# src/preprocess.py

import json
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def preprocess_text(text):
    # Initialize lemmatizer and stopwords
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    
    # Lowercase
    text = text.lower()
    # Remove punctuation and special characters
    text = re.sub(r'[^\w\s]', '', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    # Tokenize
    tokens = nltk.word_tokenize(text)
    # Remove stopwords and lemmatize
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    # Join tokens back into string
    preprocessed_text = ' '.join(tokens)
    return preprocessed_text

def preprocess_data(input_file='data/faq_data.json', output_file='data/processed_faq_data.json'):
    # Load data from JSON file
    with open(input_file, 'r', encoding='utf-8') as f:
        faq_data = json.load(f)
    
    # Preprocess questions and answers
    for entry in faq_data:
        entry['processed_question'] = preprocess_text(entry['title'])
        entry['processed_answer'] = preprocess_text(entry['content'])
    
    # Save processed data to new JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(faq_data, f, ensure_ascii=False, indent=4)
    
    print(f"Preprocessed data saved to {output_file}")

if __name__ == '__main__':
    preprocess_data()
