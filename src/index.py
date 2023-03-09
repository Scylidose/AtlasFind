import csv
import os
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT
from whoosh.qparser import QueryParser


def create_database(input_data, db_dir):
    # Create an index
    schema = Schema(title=TEXT(stored=True), content=TEXT(stored=True))
    if not os.path.exists(db_dir):
        os.mkdir(db_dir)
    ix = create_in(db_dir, schema)
    writer = ix.writer()
    with open(input_data) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            writer.add_document(title=row['Link'], content=row['Text'])
    writer.commit()

    return ix


def search_query(queryText, index):
    # Search the index
    searcher = index.searcher()
    query = QueryParser("content", index.schema).parse(queryText)
    results = searcher.search(query)

    # Return relevant documents
    for hit in results:
        print(hit['title'])
