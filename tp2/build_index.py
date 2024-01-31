# build_index.py

import json

def build_inverse_index(tokenized_titles):
    inverse_index = {}
    for doc_id, tokens in enumerate(tokenized_titles):
        for token in tokens:
            if token not in inverse_index:
                inverse_index[token] = []
            if doc_id not in inverse_index[token]:
                inverse_index[token].append(doc_id)
    return inverse_index

def save_index_to_json(inverse_index, filename):
    with open(filename, 'w') as file:
        json.dump(inverse_index, file, indent=4)
