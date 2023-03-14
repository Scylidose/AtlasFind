from django.shortcuts import render
from django.http import JsonResponse

import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'src')))

import answer

# Create your views here.
def home(request):
    return render(request, 'search.html', {'results': ''})

def search(request):
    # retrieve the search query from the request
    search_query = request.GET.get('search_query', None)
    # perform search and retrieve results
    results = answer.answer_question(search_query)

    # prepare the data to be sent back to the client
    if not results:
        results = ''
    
    data = {
        'results': results,
    }

    # return the data as JSON response
    return JsonResponse(data)
