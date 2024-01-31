
```markdown
# Constructing a Minimal Index

## Overview

This project ,titled "Constructing a Minimal Index", is an academic endeavor assigned by Lara Perinetti for the Web Indexing course at ENSAI. The primary goal of this project is to develop a minimal index for a set of web-crawled data. The project includes Python scripts for reading JSON data, preprocessing text, tokenizing and stemming (French language because most of the sites in the crawler_web.json are in french )and constructing both inverse and positional indices.

## Installation

Before running the project, ensure that Python is installed on your system. This project requires specific Python packages from NLTK, a leading platform for building Python programs to work with human language data.

### Required Python Packages

Install the necessary Python packages using `pip`:

```bash
pip install nltk
pip install json
pip install re
pip install unicodedata
pip install collections
```

### NLTK Data

After installing NLTK, you need to download specific datasets used by NLTK, particularly for tokenization and stemming in French:

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

These commands will download the required tokenizers and stopwords data for processing French text.

## Project Structure

The project is structured as follows:

- `main.py`: The main script that orchestrates reading data, processing, and indexing.
- `build_index.py`: Contains functions to build both inverse and positional indices.
- `statistics_and_stem.py`: Includes functions for preprocessing text, tokenization, stemming, and generating basic statistics.
- `comparing_stemmers.py`: Includes a comparison for different stemmers to justify the chosen stimmer.

Make sure to clone the repository into a directory named `TP2_min_index` to maintain consistency with the project structure.

## Cloning and Running the Project

To clone and run the project, follow these steps:

1. Open your terminal.
2. Change to the directory where you want to clone the project.
3. Run the following command to clone the project:
   
   ```bash
   git clone git@github.com:Wa101001/Indexation-Web.git tp2
   ```

4. Change to the `tp2` directory:

   ```bash
   cd tp2
   ```

5. Execute the main script:

   ```bash
   python main.py
   ```

This will run the main script, which reads the data, processes it, and builds the indices as specified.

