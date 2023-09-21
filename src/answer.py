from . import index, model

models = {
    "gpt-3.5-4k-tokens": {
        "name": "gpt-3.5-turbo", 
        "token_length": 4096,
        "input_cost": 0.0015,
        "output_cost": 0.002,
        "available": True 
    },
    "gpt-3.5-16k-tokens": {
        "name": "gpt-3.5-turbo-16k", 
        "token_length": 16384,
        "input_cost": 0.003,
        "output_cost": 0.004,
        "available": True 
    }
}

def answer_question(model_choice, model_object, query_text, output_file, db_dir):
    """
    Use the specified model to answer a question based on the given query text.

    Args:
        model_choice (str): The name of the model to use for answering the question. Must be either "DeepPavlov"
            or "ChatHPT".
        model_object: An instance of the model to use. For DeepPavlov, this should be an instance of the
            `deeppavlov.models.bertqa.BertQA` class.
        query_text (str): The text of the question to answer.
        output_file (str): The path to the file where the search index should be saved (only used for DeepPavlov).
        db_dir (str): The path to the directory where the search index should be stored (only used for DeepPavlov).

    Returns:
        The answer to the question, as determined by the specified model. If the model is unable to find an
        answer, returns an empty string.
    """
    
    index_db = index.create_database(output_file, db_dir)
    if query_text is None:
        query_text = ''

    documents = index.search_query(query_text, index_db)

    if model_choice == "DeepPavlov":
        if len(documents) > 0:
            return model.deeppavlov_answer(model_object, body, query_text)
    else:
        body = ' '.join(item['content'] for item in documents)
        negResponse = "I'm unable to answer the question based on the information I have."

        prompt = f"Answer this question: {query_text}\nUsing only the information from this documentation: {body}\nIf the answer is not contained in the supplied doc reply '{negResponse}' and nothing else"
        
        truncated_prompt = model.configure_gpt(prompt, models[model_choice], 1024)

        if model_choice.startswith("gpt"):
            return model.chat_with_gpt(truncated_prompt, models[model_choice])

    return ''