# src/synonyms.py

from nltk.corpus import wordnet
import nltk

def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonym = lemma.name().replace('_', ' ').lower()
            if synonym != word:
                synonyms.add(synonym)
    return synonyms

def expand_query(query):
    tokens = query.split()
    expanded_tokens = tokens.copy()
    for token in tokens:
        syns = get_synonyms(token)
        expanded_tokens.extend(syns)
    expanded_query = ' '.join(set(expanded_tokens))
    return expanded_query

if __name__ == '__main__':
    # Example usage
    query = "account recovery"
    expanded = expand_query(query)
    print(f"Original query: {query}")
    print(f"Expanded query: {expanded}")
