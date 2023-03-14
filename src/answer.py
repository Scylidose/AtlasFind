import index, model

def answer_question(model_choice, model_object, query_text, output_file, db_dir):

    if model_choice == "DeepPavlov":
        index_db = index.create_database(output_file, db_dir)
        if query_text is None:
            query_text = ''

        documents = index.search_query(query_text, index_db)

        if len(documents) > 0:
            return model.deeppavlov_answer(model_object, documents[0]['content'], query_text)

    elif model_choice == "Haystack":
        return model.haystack_answer(model_object, query_text)

    return ''