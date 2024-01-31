import json
from statistics_and_stem import read_json_file, tokenize_titles, generate_statistics, preprocess_text, tokenize_and_stem_titles
from build_index import build_inverse_index, build_positional_index



def custom_json_serializer(data):
    """ Custom serialization to put each list on a single line """
    parts = []
    for key, value in data.items():
        serialized_value = json.dumps(value)
        parts.append(f'    "{key}": {serialized_value}')
    return "{\n" + ",\n".join(parts) + "\n}"

def save_index_to_json(data, filename):
    with open(filename, 'w') as file:
        file.write(custom_json_serializer(data))
def main():
    file_path = 'crawled_urls.json'
    data = read_json_file(file_path)

    # Generate statistics
    tokenized_titles = tokenize_titles(data)
    stats = generate_statistics(data, tokenized_titles)
    save_index_to_json(stats, 'metadata.json')
    print("Statistics saved to metadata.json")

    # Build the original inverse index (without stemming)
    inverse_index = build_inverse_index(tokenized_titles)
    save_index_to_json(inverse_index, 'title.non_pos_index.json')
    print("Original Inverse index saved to title.non_pos_index.json")
    # BUild the stemmed inverse index
    stemmed_titles = tokenize_and_stem_titles(data)
    stemmed_inverse_index = build_inverse_index(stemmed_titles)
    save_index_to_json(stemmed_inverse_index, 'mon_stemmer.title.non_pos_index.json')
    print("Stemmed Inverse index saved to mon_stemmer.non_index_pos.json")

    positional_index = build_positional_index(tokenized_titles)
    save_index_to_json(positional_index, 'title.pos_index.json')
    print("Positional index saved to title.pos_index.json")

if __name__ == "__main__":
    main()
