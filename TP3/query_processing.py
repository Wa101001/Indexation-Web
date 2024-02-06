# query_processing.py
import json

def load_json_file(file_path):
    """Load a JSON file from the specified file path."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def tokenize_query(query):
    """Tokenize the query string into a list of tokens."""
    return query.lower().split()

def filter_documents(index, query_tokens, filter_type='AND'):
    filtered_doc_ids = None

    if filter_type == 'AND':
        for token in query_tokens:
            if token in index:
                if filtered_doc_ids is None:
                    filtered_doc_ids = set(index[token])
                else:
                    filtered_doc_ids &= set(index[token])
            else:
                return set()  # If any token is not found, return an empty set

    elif filter_type == 'OR':
        for token in query_tokens:
            if token in index:
                if filtered_doc_ids is None:
                    filtered_doc_ids = set(index[token])
                else:
                    filtered_doc_ids |= set(index[token])

    return filtered_doc_ids if filtered_doc_ids is not None else set()
