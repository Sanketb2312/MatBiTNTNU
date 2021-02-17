from django.http import HttpResponse
from django.shortcuts import render
from django.template import Context, loader

# Create your views here.

def frontpage(request):
    return render(request, 'frontpage.html')

def register(request):
    template = loader.get_template("registerUser.html")
    return HttpResponse(template.render())

