# query_processing.py
import json

def load_json_file(file_path):
    """Load a JSON file from the specified file path."""
    # Opens the file, reads its content as JSON and returns the parsed JSON data
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def tokenize_query(query):
    """Tokenize the query string into a list of tokens."""
    # Converts the query to lowercase and splits it into words based on spaces
    return query.lower().split()

def filter_documents(index, query_tokens, filter_type='AND'):
    # Initialize a variable to hold the filtered document IDs
    filtered_doc_ids = None

    # If the filter type is 'AND', perform intersection of document ID sets
    if filter_type == 'AND':
        for token in query_tokens:
            if token in index:
                # For the first token, initialize filtered_doc_ids with its document IDs
                if filtered_doc_ids is None:
                    filtered_doc_ids = set(index[token])
                else:
                    # For subsequent tokens, intersect the sets to narrow down the results
                    filtered_doc_ids &= set(index[token])
            else:
                # If any token is not found, return an empty set as no document matches the full query
                return set()

    # If the filter type is 'OR', perform union of document ID sets
    elif filter_type == 'OR':
        for token in query_tokens:
            if token in index:
                # For the first token, initialize filtered_doc_ids with its document IDs
                if filtered_doc_ids is None:
                    filtered_doc_ids = set(index[token])
                else:
                    # For subsequent tokens, unite the sets to expand the results
                    filtered_doc_ids |= set(index[token])

    # Return the final set of filtered document IDs or an empty set if none matched
    return filtered_doc_ids if filtered_doc_ids is not None else set()
