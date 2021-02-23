from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.utils import timezone
from .mymodels import Bruker, Arrangement


def is_logged_in(request):
    if 'user_id_logged_in' in request.session:
        site_logged_in = True
    else:
        site_logged_in = False
    return site_logged_in

# Create your views here.

def frontpage(request):
    return render(request, 'frontpage.html', {'site_logged_in' : is_logged_in(request)})

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
            return redirect('/')

    return render(request, "registerUser.html", {'emailUsed' : emailUsed, 'first_name':first_name, 'last_name':last_name,
                                                 'birth_date':birth_date, 'address':address, 'post_code':post_code, 'place':place, 'site_logged_in' : is_logged_in(request)})

def login(request):
    logged_in = False
    error_login = False
    user_id = 0
    if request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = Bruker.objects.get(epost=email, passord=password)
            logged_in = True
        except:
            error_login = True
        if logged_in:
            user_id = user.brukerid
            request.session['user_id_logged_in'] = user_id
            return redirect('/')
    return render(request, 'login.html', {'error_login' : error_login, 'site_logged_in' : is_logged_in(request)})

def logout(request):
    if is_logged_in(request):
        del request.session['user_id_logged_in']
    else:
        return redirect('/')
    return redirect('/')

def profile(request):
    if is_logged_in(request):
        print("hei")
    else:
        return redirect('/')
    return render(request, 'profile.html', {'site_logged_in' : is_logged_in(request)})

def newMeal(request):
    if request.POST:
        arrangement_name = request.POST.get('arrangement_name')
        description = request.POST.get('description')
        seats = request.POST.get('seats')
        location = request.POST.get('location')
        time = request.POST.get('time')
        prize = request.POST.get('prize')

        newMeal = Arrangement(arrangementnavn = arrangement_name, beskrivelse = description, antallplasser =seats, lokasjon = location,
                              tidspunkt = time, opprettet = timezone.now(), pris = prize, avlyst = 0)
        newMeal.save()


    return render(request, 'newMeal.html', {'site_logged_in' : is_logged_in(request)})

def mealOverview(request):

    queryset = Arrangement.objects.all()

    return render(request, 'mealOverview.html', {"object_list" : queryset, 'site_logged_in' : is_logged_in(request)})
