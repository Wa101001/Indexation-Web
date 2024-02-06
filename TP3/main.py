from query_processing import tokenize_query, filter_documents, load_json_file
from ranking import rank_documents
import json
def main(query):
    # Load indexes and documents
    title_index = load_json_file('title_pos_index.json')
    content_index = load_json_file('content_pos_index.json')
    documents = load_json_file('documents.json')

    # Tokenize the query
    query_tokens = tokenize_query(query)

    # Ask the user to choose the filter type ('AND' or 'OR')
    filter_type = input("Choose filter type ('AND' or 'OR'): ").strip().upper()

    # Validate the filter type
    if filter_type not in ['AND', 'OR']:
        print("Invalid filter type. Please choose 'AND' or 'OR'.")
        return

    # Filter documents based on the selected filter type
    filtered_doc_ids = filter_documents({**title_index, **content_index}, query_tokens, filter_type)

    # Rank documents based on a linear function
    ranked_doc_ids = rank_documents(filtered_doc_ids, title_index, content_index)

    # Rank documents based on a linear function
    ranked_doc_ids = rank_documents(filtered_doc_ids, title_index, content_index)

 # Prepare the output
    results = []
    for doc_id in ranked_doc_ids:
        doc_info = next((doc for doc in documents if str(doc['id']) == str(doc_id)), None)  # Ensure ID types match
        if doc_info:
            results.append({"Title": doc_info['title'], "URL": doc_info['url']})

    # Output the results including the total number of documents and number of filtered documents
    output = {
        "total_documents": len(documents),
        "filtered_documents": len(filtered_doc_ids),
        "results": results
    }

    # Write the output to a file
    with open('results.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)

# Example usage
if __name__ == "__main__":
    query = input("Please provide a query:")  
    main(query)

