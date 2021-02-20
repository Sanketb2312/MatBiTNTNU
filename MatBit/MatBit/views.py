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
            user = Bruker(fornavn=first_name, etternavn = last_name, fodselsdato = birth_date, adresse = address, postnummer = post_code,
                          sted = place, eradministrator = "0", epost = email, passord = password)
            user.save()
            return render(request, "frontpage.html")

    return render(request, "registerUser.html", {'emailUsed' : emailUsed, 'first_name':first_name, 'last_name':last_name,
                                                 'birth_date':birth_date, 'address':address, 'post_code':post_code, 'place':place})

def logginn(request):
    logged_in = False
    error_login = False
    if request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            Bruker.objects.get(epost=email, passord=password)
            logged_in = True
            return render(request, "frontpage.html")
        except:
            error_login = True
    return render(request, 'logginn.html', {'logged_in' : logged_in, 'error_login' : error_login})
