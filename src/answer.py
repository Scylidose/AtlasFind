import index, model

def answer_question(model_choice, model_object, query_text, output_file, db_dir):
    """
    Use the specified model to answer a question based on the given query text.

    Args:
        model_choice (str): The name of the model to use for answering the question. Must be either "DeepPavlov"
            or "Haystack".
        model_object: An instance of the model to use. For DeepPavlov, this should be an instance of the
            `deeppavlov.models.bertqa.BertQA` class. For Haystack, this should be an instance of the `ExtractiveQAPipeline`
            class.
        query_text (str): The text of the question to answer.
        output_file (str): The path to the file where the search index should be saved (only used for DeepPavlov).
        db_dir (str): The path to the directory where the search index should be stored (only used for DeepPavlov).

    Returns:
        The answer to the question, as determined by the specified model. If the model is unable to find an
        answer, returns an empty string.
    """
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