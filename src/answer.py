import index #, model

def answer_question(query_text):
    output_file = "../data/links.csv"
    db_dir = "../data/whoosh"

    index_db = index.create_database(output_file, db_dir)
    if query_text is None:
        query_text = 'No Man\s sky'
    print("---> ", query_text)
    documents = index.search_query(query_text, index_db)
    if len(documents) > 0:
        return [documents[0]['title']]
    else: 
        return 'No Man\s Sky was created in August 2016'
    #model.answer_question(documents[0]['content'], query_text)
