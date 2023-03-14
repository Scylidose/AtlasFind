from deeppavlov import build_model, configs

from haystack.document_stores import InMemoryDocumentStore
from haystack.pipelines.standard_pipelines import TextIndexingPipeline
from haystack.nodes import BM25Retriever, FARMReader
from haystack.pipelines import ExtractiveQAPipeline
from haystack.utils import print_answers

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

def configure_haystack(doc_dir):
    """
    Configure a Haystack Extractive Question Answering (QA) Pipeline.

    The function uses a directory containing text documents to create an in-memory document store, index the
    documents using BM25, load a pre-trained FARM Reader model for extractive QA, and create a pipeline that combines
    the reader and the retriever.

    Args:
        doc_dir (str): The path to the directory containing the text documents to be indexed and searched.

    Returns:
        A Haystack ExtractiveQAPipeline object that can be used to perform extractive QA.
    """
    document_store = InMemoryDocumentStore(use_bm25=True)

    files_to_index = [doc_dir + "/" + f for f in os.listdir(doc_dir)]
    indexing_pipeline = TextIndexingPipeline(document_store)
    indexing_pipeline.run_batch(file_paths=files_to_index)

    retriever = BM25Retriever(document_store=document_store)

    reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2", use_gpu=True)

    return ExtractiveQAPipeline(reader, retriever)


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

model = build_model(configs.squad.squad_bert)


def haystack_answer(pipe, query):
    """
    Use a Haystack Extractive Question Answering (QA) Pipeline to answer a question.

    The function takes a query (a question) and uses the Haystack pipeline to retrieve the top-k most relevant
    documents from the in-memory document store using BM25, and then use a pre-trained FARM Reader model for extractive
    QA to extract the answer from the retrieved documents.

    Args:
        pipe (ExtractiveQAPipeline): A Haystack ExtractiveQAPipeline object configured with a retriever and a reader.
        query (str): The question to be answered.

    Returns:
        The extracted answer to the question.
    """
    prediction = pipe.run(
        query=query,
        params={
            "Retriever": {"top_k": 10},
            "Reader": {"top_k": 5}
        }
    )

    return prediction['answers'][0].answer
