# statistics.py

import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import nltk
from collections import Counter

# Make sure to download the necessary NLTK data


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def preprocess_text(text):
    # Remove non-alphanumeric characters and lower the case
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())
    return text

def tokenize_titles(data):
    # Update the French stop words list
    additional_stopwords = {'a', 'e','re','r'}  # Add any other tokens you want to filter out
    french_stopwords = set(stopwords.words('french')).union(additional_stopwords)
    
    titles = [preprocess_text(item['title']) for item in data]
    tokenized_titles = [word_tokenize(title, language='french') for title in titles]
    # Remove stopwords
    tokenized_titles = [[word for word in title if word not in french_stopwords] for title in tokenized_titles]
    return tokenized_titles

def generate_statistics(data, tokenized_titles, top_n=10, rare_n=10):
    num_documents = len(tokenized_titles)
    total_tokens = sum(len(tokens) for tokens in tokenized_titles)
    avg_tokens_per_doc = total_tokens / num_documents if num_documents else 0

    token_frequency = Counter(token for title in tokenized_titles for token in title)
    top_n_tokens = token_frequency.most_common(top_n)
    rare_n_tokens = token_frequency.most_common()[:-rare_n-1:-1]  # Getting the least common tokens

    statistics = {
        "Number of Documents": num_documents,
        "Total Number of Tokens": total_tokens,
        "Average Tokens per Document": avg_tokens_per_doc,
        "Top 10 Frequent Tokens": top_n_tokens,
        "Top 10 Rare Tokens": rare_n_tokens
    }

    return statistics

