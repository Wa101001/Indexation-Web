import nltk
from nltk.stem import *
import nltk
from nltk.stem import *

def stemmer_isri(token):
    stemmer_isri = nltk.stem.isri.ISRIStemmer()
    stemmed_token_isri =stemmer_isri.stem(token)
    return stemmed_token_isri
def stemmer_lancaster(token):
    stemmer_lancaster = nltk.stem.lancaster.LancasterStemmer()
    stemmed_token_lancaster =stemmer_lancaster.stem(token)
    return stemmed_token_lancaster
def stemmer_porter(token):
    stemmer_porter = nltk.stem.porter.PorterStemmer()
    stemmed_token_porter =stemmer_porter.stem(token)
    return stemmed_token_porter
def stemmer_regexp(token):
    stemmer_regexp = nltk.stem.regexp.RegexpStemmer('[^a-zA-Z0-9]+', min=4)
    stemmed_token_regexp =stemmer_regexp.stem(token)
    return stemmed_token_regexp 

def stemmer_snowball(token):
    stemmer_snowball = nltk.stem.snowball.FrenchStemmer()
    stemmed_token_snowball =stemmer_snowball.stem(token)
    return  stemmed_token_snowball

# Sample tokens to test the stemmers
sample_tokens = ["manger", "mangeais", "manges", "mangé", "mangerai","erreur","comment"]

# Initialize stemmers
stemmer_functions = {
    "ISRI Stemmer": stemmer_isri,
    "Lancaster Stemmer": stemmer_lancaster,
    "Porter Stemmer": stemmer_porter,
    "Regexp Stemmer": stemmer_regexp,
    "Snowball Stemmer": stemmer_snowball
}

# Test and compare the stemmers
for stemmer_name, stemmer_function in stemmer_functions.items():
    print(f"Testing {stemmer_name}:")
    stemmed_tokens = [stemmer_function(token) for token in sample_tokens]
    print(stemmed_tokens)
    print()


