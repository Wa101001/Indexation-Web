import json
from statistics_and_stem import read_json_file, tokenize_titles, generate_statistics, tokenize_and_stem_titles
from build_index import build_inverse_index, build_positional_index


# Define a custom JSON serializer to format JSON data so that each list occupies one line
def custom_json_serializer(data):
    # empty list 
    parts = []
    # Iterate through key-values
    for key, value in data.items():
        # Serialize the value to a JSON formatted string
        serialized_value = json.dumps(value)
        parts.append(f'    "{key}": {serialized_value}')
    # Combine all parts into a single string with proper JSON structure
    return "{\n" + ",\n".join(parts) + "\n}"

# Define a function to save data to a JSON file using the custom serializer
def save_index_to_json(data, filename):

    with open(filename, 'w') as file:
        # Write the serialized data to the file
        file.write(custom_json_serializer(data))

def main():
    # Path to the JSON file containing the crawled URLs make sure you are working in ~/Indexation-web/tp2
    file_path = 'crawled_urls.json'
    # Read data from the JSON file
    data = read_json_file(file_path)

    # Tokenize the titles from the data
    tokenized_titles = tokenize_titles(data)
    # Generate statistics from the tokenized titles
    stats = generate_statistics(data, tokenized_titles)
    # Save the statistics to a JSON file
    save_index_to_json(stats, 'metadata.json')
    print("Statistics saved to metadata.json")

    # Build an inverse index from the tokenized titles
    inverse_index = build_inverse_index(tokenized_titles)
    # Save the inverse index to a JSON file
    save_index_to_json(inverse_index, 'title.non_pos_index.json')
    print("Original Inverse index saved to title.non_pos_index.json")
    # Build the stemmed inverse index
    stemmed_titles = tokenize_and_stem_titles(data)
    stemmed_inverse_index = build_inverse_index(stemmed_titles)
    save_index_to_json(stemmed_inverse_index, 'mon_stemmer.non_index_pos.json')
    print("Stemmed Inverse index saved to mon_stemmer.non_index_pos.json")

    # Build a positional index from the tokenized titles
    positional_index = build_positional_index(tokenized_titles)
    # Save the positional index to a JSON file
    save_index_to_json(positional_index, 'title.pos_index.json')
    print("Positional index saved to title.pos_index.json")


if __name__ == "__main__":
    main()
