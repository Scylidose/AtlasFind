from deeppavlov import build_model, configs


model = build_model(configs.squad.squad_bert)

def answer_question(documents, query):
    """
    Answer a question based on a list of documents and a query using DeepPavol model.

    Args:
        documents (list): A list of documents as strings to search for an answer.
        query (str): A string representing the question being asked.

    Returns:
        The answer to the question based on the input documents.
    """
    #document_list = []
    #for hit in documents:
    #    document_list.append(hit)
    #documents = "\n\n".join(document_list)

    if not isinstance(documents, list):
        documents = [documents]

    if not isinstance(query, list):
        query = [query]

    answer = model(documents, query)

    return answer
