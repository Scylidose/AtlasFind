from deeppavlov import build_model, configs
import openai
from . import preprocess

import os

def configure_deeppavlov():
    """
    Configure a DeepPavlov Question Answering (QA) Model.

    The function loads a pre-trained BERT-based model for extractive QA from the DeepPavlov library.

    Returns:
        A DeepPavlov SquadModel object that can be used to perform
        extractive QA.
    """
    return build_model(configs.squad.squad_bert)

def deeppavlov_answer(model, documents, query):
    """
    Answer a question based on a list of documents and a query using DeepPavol model.

    Args:
        documents (list): A list of documents as strings to search for an answer.
        query (str): A string representing the question being asked.

    Returns:
        The answer to the question based on the input documents.
    """

    if not isinstance(documents, list):
        documents = [documents]

    if not isinstance(query, list):
        query = [query]

    answer = model(documents, query)

    return answer

def configure_gpt(message, model, max_tokens):
    """
    Configure a GPT-based language model for generating responses to a message.

    Args:
        message (str): The input message or prompt.
        model (dict): A dictionary representing the GPT model, including its properties.
        max_tokens (int): The maximum number of tokens allowed in the generated response.

    Returns:
        str: A truncated input message suitable for GPT-based model generation.
    """
    safety_margin = int(model['token_length']*0.25)
    truncated_prompt, word_count = preprocess.truncate_text(message, model['token_length'] - max_tokens - safety_margin)
    
    return truncated_prompt

def chat_with_gpt(message, model):
    """
    Generate a response using GPT-based chat capabilities.

    Args:
        message (list): A list of message objects with 'role' and 'content'.
        model (dict): A dictionary containing the GPT-based chat model information.

    Returns:
        str: A generated response based on the input messages.
    """
    response = openai.ChatCompletion.create(
        model=model['name'],
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message}
                ]
    )

    return response.choices[0].message.content
