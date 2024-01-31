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



def build_positional_index(tokenized_titles):
    positional_index = {}
    for doc_id, tokens in enumerate(tokenized_titles):
        for position, token in enumerate(tokens):
            if token not in positional_index:
                positional_index[token] = {}
            if doc_id not in positional_index[token]:
                positional_index[token][doc_id] = []
            positional_index[token][doc_id].append(position)
    return positional_index

