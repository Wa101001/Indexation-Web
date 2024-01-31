import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import unicodedata
import re
from collections import Counter

# Function to read and load data from a JSON file
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# Function to preprocess text data
def preprocess_text(text):
    # Normalize text to remove accents and diacritics
    text = ''.join(c for c in unicodedata.normalize('NFD', text)
                   if unicodedata.category(c) != 'Mn')
    
    # Remove non-alphanumeric characters and convert to lowercase
    text = re.sub(r'[^a-zA-Z0-9àâçéèêëîïôûùüÿñæœ]', ' ', text.lower())
    
    # Replace multiple spaces with a single space and strip leading/trailing spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

# Function to tokenize titles from the data
def tokenize_titles(data):
    # French stopwords, I added the additional_stopwords list for the tokens that have a high frequency and low relevancy 
    additional_stopwords = {'a', 'e', 're', 'r'}
    french_stopwords = set(stopwords.words('french')).union(additional_stopwords)
    
    # Preprocess and tokenize each title in the data
    titles = [preprocess_text(item['title']) for item in data]
    tokenized_titles = [word_tokenize(title, language='french') for title in titles]
    
    # Remove stopwords from tokenized titles
    tokenized_titles = [[word for word in title if word not in french_stopwords] for title in tokenized_titles]
    return tokenized_titles

# Function to tokenize and stem titles
def tokenize_and_stem_titles(data):
    # Stopwords
    additional_stopwords = {'a', 'e', 're', 'r'}
    french_stopwords = set(stopwords.words('french')).union(additional_stopwords)
    
    # Initialize the French stemmer, I based this choice on the results of the comparing_stemmers.py file
    stemmer = SnowballStemmer("french")
    
    # Preprocess and tokenize titles
    titles = [preprocess_text(item['title']) for item in data]
    tokenized_titles = [word_tokenize(title, language='french') for title in titles]

    # Remove stopwords and apply stemming
    stemmed_titles = []
    for title in tokenized_titles:
        stemmed_title = [stemmer.stem(word) for word in title if word not in french_stopwords]
        stemmed_titles.append(stemmed_title)
    
    return stemmed_titles

# Function to generate various statistics from tokenized titles
def generate_statistics(data, tokenized_titles, top_n=10, rare_n=10):
    # Calculate the demanded statistics
    num_documents = len(tokenized_titles)
    total_tokens = sum(len(tokens) for tokens in tokenized_titles)
    avg_tokens_per_doc = total_tokens / num_documents if num_documents else 0

    # Count frequency of each token
    token_frequency = Counter(token for title in tokenized_titles for token in title)
    
    # Identify most and least common tokens
    top_n_tokens = token_frequency.most_common(top_n)
    rare_n_tokens = token_frequency.most_common()[:-rare_n-1:-1]

    # Compile statistics into a dictionary
    statistics = {
        "Number of Documents": num_documents,
        "Total Number of Tokens": total_tokens,
        "Average Tokens per Document": avg_tokens_per_doc,
        "Top 10 Frequent Tokens": top_n_tokens,
        "Top 10 Rare Tokens": rare_n_tokens
    }

    return statistics
