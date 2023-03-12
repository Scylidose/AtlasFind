from django.shortcuts import render
import sys, os
sys.path.append(os.path.abspath(os.path.join('..', 'src')))

import answer

# Create your views here.
def home(request):
    query = request.GET.get('q')
    results = answer.answer_question(query)
    return render(request, 'search_results.html', {'results': results})
