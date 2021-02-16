from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

def test(request):
    # if this is a POST request we need to process the form data
    return render(request, 'checklist/test.html', {})

