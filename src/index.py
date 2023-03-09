import csv
import os
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser


def create_database(input_data, db_dir):
    """
    Create or open an index for full-text search, and populate it with data from a CSV file.

    Args:
        input_data (str): A path to the CSV file containing the data to be indexed.
        db_dir (str): A path to the directory where the index will be created or opened.

    Returns:
        An instance of the Index class from the Whoosh library, representing the index that was created or opened.
    """
    # Create an index
    schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True))
    if not os.path.exists(db_dir):
        os.mkdir(db_dir)
        idx = create_in(db_dir, schema)
        writer = idx.writer()
        with open(input_data, encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                writer.add_document(title=row['Link'], content=row['Text'])
        writer.commit()
    else:
        idx = open_dir(db_dir)
    return idx


def search_query(queryText, idx):
    """
    The function search_query searches an existing index for a given query text and returns the search results.

    Args:
        queryText (str): The query text to search for.
        idx (Index): An existing Index object representing the index to search.

    Returns:
        A SearchResults object containing the search results. The results are sorted by relevance, with the most relevant document first. Each result is a Hit object, which contains information about the document, such as its score, stored field values, and more.
    """
    # Search the index
    searcher = idx.searcher()
    query = QueryParser("content", idx.schema).parse(queryText)
    results = searcher.search(query)

    return results
