from nltk.stem import SnowballStemmer
from statistics import preprocess_text

def stem_text(data):
    stemmer_snowball = SnowballStemmer("french")

    tokenized_titles_with_stemming = [stemmer_snowball.stem(preprocess_text(item['title'])) for item in data]

    return tokenized_titles_with_stemming
