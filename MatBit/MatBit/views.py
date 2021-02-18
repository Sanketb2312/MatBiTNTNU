from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def frontpage(request):
    return render(request, 'frontpage.html')

