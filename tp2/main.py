import json
from statistics import read_json_file, tokenize_titles, generate_statistics, preprocess_text
from build_index import build_inverse_index, save_index_to_json
from stemmer import stem_text  # Import stem_text function from stemmer.py

def save_statistics_to_json(statistics, filename):
    with open(filename, 'w') as file:
        json.dump(statistics, file, indent=4)

def main():
    file_path = 'crawled_urls.json'
    data = read_json_file(file_path)

    # Generate statistics
    tokenized_titles = tokenize_titles(data)
    stats = generate_statistics(data, tokenized_titles)
    save_statistics_to_json(stats, 'metadata.json')
    print("Statistics saved to metadata.json")

    # Build the original inverse index (without stemming)
    inverse_index = build_inverse_index(tokenized_titles)
    save_index_to_json(inverse_index, 'title.non_pos_index.json')
    print("Original Inverse index saved to title.non_pos_index.json")


if __name__ == "__main__":
    main()
