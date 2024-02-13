# Query expansion and ranking

This project provides a simple yet effective way to search and rank documents based on user queries. It consists of two main components: query processing and document ranking, including an implementation of the BM25 algorithm for sophisticated ranking capabilities.

## Features

- **Query Processing**: Tokenizes user queries and filters documents based on the presence of query tokens.
- **Document Ranking**: Ranks the filtered documents based on the occurrences of query tokens in the document titles and content. It also includes an option to use the BM25 algorithm for ranking, which considers document length and term frequency-inverse document frequency (TF-IDF) principles.

## Requirements

To run this project, you need Python 3.x and the following Python package:

- `rank_bm25`: A Python package that implements the BM25 ranking algorithm.

To install the required package, run:

```bash
pip install -r requirements.txt
```

## Usage

0. **To avoid all path problems make sure you are working in the Indexation-Web/TP3 repository** to do that just execute the command ```cd TP3``` in the terminal.
1. **Run the Main Script**: Execute `main.py` and follow the prompts to input your query and select the filter type (`AND`/`OR`). 

2. **Review Results**: The script will output the ranked documents based on your query, which includes the document titles and URLs.

## Components

- `main.py`: Orchestrates the query processing and document ranking process.
- `query_processing.py`: Contains functions for loading JSON data, tokenizing queries, and filtering documents based on query tokens.
- `ranking.py`: Includes functions for ranking documents based on simple occurrence counts and the BM25 algorithm.

## Detailed Ranking Functions Explanation

This system employs two distinct approaches for ranking documents: a simple occurrence-based method and the BM25 algorithm. Each method evaluates the relevance of documents to a user's query differently, ensuring flexibility and effectiveness in search results.

### Simple Occurrence-Based Ranking

This method, implemented in `rank_documents`, scores documents based on the frequency of query tokens within document titles and content. Each occurrence of a token contributes to the document's score, with tokens in the title receiving a higher weight to reflect their importance. The function processes each document in the filtered set, accumulating scores based on these criteria:

- **Title Weighting**: Tokens found in the title are considered more significant, thus are weighted more heavily in the scoring process. This reflects the intuition that the title of a document is a strong indicator of its overall content and relevance.
- **Content Consideration**: Tokens within the content also contribute to the score, ensuring a comprehensive evaluation of the document's relevance to the query.

After scoring, documents are sorted in descending order of their scores, with higher scores indicating greater relevance to the query.

### BM25 Ranking Algorithm

The `rank_documents_bm25` function utilizes the BM25 algorithm, a more sophisticated approach that considers document length and the inverse document frequency of query tokens. This method is particularly effective in handling the variability of document lengths and the distribution of terms across a document corpus. The key steps in this process include:

- **Tokenization**: Both the documents (specifically, their titles for simplicity) and the query are tokenized to break down the text into manageable pieces for analysis.
- **BM25 Model Initialization**: The BM25 model is initialized with the tokenized documents, preparing it for scoring.
- **Scoring**: The model calculates scores for each document based on the tokenized query, taking into account the frequency of query tokens in the documents and their lengths.
- **Ranking**: Documents are ranked based on their BM25 scores, with higher scores indicating a better match between the document and the query.

By employing the BM25 algorithm, the system can effectively rank documents in a manner that is both responsive to the query's specifics and reflective of the inherent properties of the document set.





