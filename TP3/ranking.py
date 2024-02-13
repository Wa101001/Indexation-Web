# ranking.py
from query_processing import tokenize_query
from rank_bm25 import BM25Okapi

with open("stop_words_french.txt", "r", encoding="utf-8") as file:
    stopwords_text = file.read()

# Split the contents of the file into a list of stopwords
STOP_WORDS = stopwords_text.split()

def rank_documents(filtered_doc_ids, title_index, content_index):
    """Rank documents based on occurrences of query tokens in title and content."""
    doc_scores = {}
    
    for doc_id in filtered_doc_ids:
        score = 0
        for token, positions in title_index.items():
            if doc_id in positions:
                if token not in STOP_WORDS:
                    score += len(positions) * 2  # Assign a higher weight to meaningful tokens
                else:
                    score += len(positions)
        for token, positions in content_index.items():
            if doc_id in positions:
                if token not in STOP_WORDS:
                    score += len(positions) * 2  # Assign a higher weight to meaningful tokens
                else:
                    score += len(positions)
        doc_scores[doc_id] = score

    return sorted(doc_scores.keys(), key=lambda x: doc_scores[x], reverse=True)



def rank_documents_bm25(filtered_doc_ids, documents, query):
    # Tokenize documents
    tokenized_documents = [tokenize_query(doc['title']) for doc in documents if doc['id'] in filtered_doc_ids]

    # In case the word doesn't exist anywhere we return an empty list and we don't try to calculate the BM25 score
    if len(tokenized_documents)==0:
        print("Query not found")
        ranked_doc_ids = []
    else:
        # Initialize BM25 model
        bm25 = BM25Okapi(tokenized_documents)
        
        # Tokenize queryy
        tokenized_query = tokenize_query(query)
        
        # Calculate BM25 scores for the query against all documents
        scores = bm25.get_scores(tokenized_query)
        
        # Pair each document ID with its corresponding BM25 score
        doc_id_scores = [(doc_id, score) for doc_id, score in zip(filtered_doc_ids, scores)]
        
        # Sort documents by their BM25 score in descending order
        ranked_doc_ids = [doc_id for doc_id, score in sorted(doc_id_scores, key=lambda x: x[1], reverse=True)]
    
    return ranked_doc_ids
