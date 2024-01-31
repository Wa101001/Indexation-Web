import json

# Function to build an inverse index from tokenized titles
def build_inverse_index(tokenized_titles):
    # Empty dictionary 
    inverse_index = {}
    # Enumerate over the tokenized titles to get both doc_id and the tokens
    for doc_id, tokens in enumerate(tokenized_titles):
        # Iterate through each token in the tokens list
        for token in tokens:
            # Add the token to the inverse index if not already present and append the current doc_id to the list of document IDs for this token
            inverse_index.setdefault(token, []).append(doc_id)

    return inverse_index

# Function to build a positional index from tokenized titles
def build_positional_index(tokenized_titles):
    # Empty dictionary
    positional_index = {}
    # Enumerate over the tokenized titles to get both doc_id and the tokens
    for doc_id, tokens in enumerate(tokenized_titles):
        # Enumerate over the tokens to get both the token and its position in the list
        for position, token in enumerate(tokens):
            # Add the token to the positional index if not already present
            if token not in positional_index:
                positional_index[token] = {}
            # For each token, setdefault to initialize a list for the doc_id if not already present and append the current position to this list
            positional_index[token].setdefault(doc_id, []).append(position)

    return positional_index
