# ranking.py
def rank_documents(filtered_doc_ids, title_index, content_index):
    """Rank documents based on occurrences of query tokens in title and content."""
    doc_scores = {}
    for doc_id in filtered_doc_ids:
        score = 0
        for token, positions in title_index.items():
            if doc_id in positions:
                score += len(positions)  # Increase score by number of occurrences in title
        for token, positions in content_index.items():
            if doc_id in positions:
                score += len(positions)  # Increase score by number of occurrences in content
        doc_scores[doc_id] = score
    return sorted(doc_scores.keys(), key=lambda x: doc_scores[x], reverse=True)