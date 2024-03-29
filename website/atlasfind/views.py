from django.shortcuts import render
from django.http import JsonResponse

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'src')))

import answer, export_doc, model

documents_dir = "data/documents"
output_file = "data/links.csv"
db_dir = "data/whoosh"

export_doc.export_documents(output_file, documents_dir)
model_object = model.configure_deeppavlov()

# Create your views here.
def home(request):
    return render(request, 'search.html', {'results': ''})

def search(request):
    # retrieve the search query from the request
    search_query = request.GET.get('search_query', None)

    # perform search and retrieve results
    results = answer.answer_question("DeepPavlov", model_object, search_query, output_file, db_dir)

    # prepare the data to be sent back to the client
    if not results:
        results = ''
    
    data = {
        'results': results,
    }

    # return the data as JSON response
    return JsonResponse(data)
