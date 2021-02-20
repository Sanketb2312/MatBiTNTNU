from django.shortcuts import render, redirect
from .mymodels import Bruker


# Create your views here.

def frontpage(request):
    return render(request, 'frontpage.html')

def register(request):
    emailUsed = False
    first_name = None
    last_name = None
    birth_date = None
    address = None
    post_code = None
    place = None

    if request.POST:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        birth_date = request.POST.get('birth_date')
        password = request.POST.get('password')
        address = request.POST.get('address')
        post_code = request.POST.get('post_code')
        place = request.POST.get('place')
        try:
            Bruker.objects.get(epost=email)
            emailUsed = True

        except Exception:
            print("Du har nå lagd en ny bruker")
            return render(request, "frontpage.html")

    return render(request, "registerUser.html", {'emailUsed' : emailUsed, 'first_name':first_name, 'last_name':last_name,
                                                 'birth_date':birth_date, 'address':address, 'post_code':post_code, 'place':place})

def logginn(request):
    if request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')
    return render(request, 'logginn.html')





