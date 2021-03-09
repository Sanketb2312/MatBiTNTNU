from django.shortcuts import render, redirect
from django.contrib.auth import logout
from .mymodels import Bruker, Harallergi, Arrangement, Arrangementinnhold, Innhold, Pamelding, Vertskap
from django.utils import timezone


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
    if is_logged_in(request) == False:
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

    else:
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
        allergiDict = {}
        hostingDict = {}
        arrangementDict = {}

        user = Bruker.objects.get(brukerid = request.session['user_id_logged_in'])

        allergi = Harallergi.objects.filter(brukerid = request.session['user_id_logged_in'])
        #allergi = {'allergi' : allergi}
        for allergies in allergi:
            allergies = allergies.__dict__

            innhold = Innhold.objects.get(innholdid = allergies['innholdid'])
            allergiDict.update({innhold.innholdid : innhold.navn })

        arrangement = Pamelding.objects.filter(brukerid=request.session['user_id_logged_in'])
        for arrangements in arrangement:
            arrangements = arrangements.__dict__

            dinnerInformation = Arrangement.objects.get(arrangementid=arrangements['arrangementid'])
            arrangementDict.update({dinnerInformation.arrangementid: [dinnerInformation.arrangementnavn,
                                                                      dinnerInformation.lokasjon,
                                                                      dinnerInformation.tidspunkt]})

        hosting = Vertskap.objects.filter(brukerid=request.session['user_id_logged_in'])
        for hostingArrengement in hosting:
            hostingArrengement = hostingArrengement.__dict__

            hostingInformation = Arrangement.objects.get(arrangementid=hostingArrengement['arrangementid'])
            hostingDict.update({hostingInformation.arrangementid: [hostingInformation.arrangementnavn,
                                                                   hostingInformation.tidspunkt,
                                                                   hostingInformation.antallplasser]})
    else:
        return redirect('/')
    return render(request, 'profile.html', {'user':user,'userAllergies' : allergiDict, 'arrangement' : arrangementDict, 'hosting' : hostingDict, 'site_logged_in' : is_logged_in(request)})


def editUser(request):
    if is_logged_in(request):
        user = Bruker.objects.get(brukerid = request.session['user_id_logged_in'])

        if request.POST:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            address = request.POST.get('address')
            post_code = request.POST.get('post_code')
            place = request.POST.get('place')

            user.fornavn = first_name
            user.etternavn = last_name
            user.adresse = address
            user.postnummer = post_code
            user.sted = place
            user.save()
            return redirect('../../profil/')

    else:
        return redirect('/')
    return render(request, 'editUser.html', {'user':user,'site_logged_in': is_logged_in(request)})


def newMeal(request):
    if is_logged_in(request):
        if request.POST:
            arrangement_name = request.POST.get('arrangement_name')
            description = request.POST.get('description')
            seats = request.POST.get('seats')
            location = request.POST.get('location')
            date = request.POST.get('date')
            time = request.POST.get('time')
            prize = request.POST.get('prize')

            datetime = date+" "+time+":00"

            newMeal = Arrangement(arrangementnavn = arrangement_name, beskrivelse = description, antallplasser =seats, lokasjon = location,
                                  tidspunkt = datetime, opprettet = timezone.now(), pris = prize, avlyst = 0)
            newMeal.save()

            new_arrangemntid = newMeal.arrangementid

            host = Vertskap(brukerid = request.session['user_id_logged_in'], arrangementid = new_arrangemntid)
            host.save()

            return redirect('../../profil/')
    else:
        return redirect("/")

    return render(request, 'newMeal.html', {'site_logged_in' : is_logged_in(request)})

def mealOverview(request):
    if is_logged_in(request):
        available_dict = {}

        queryset = Arrangement.objects.all()

        #Gives the number of guests allready booked for this dinner
        for arrangements in queryset:
            arrangements = arrangements.__dict__
            guests = Pamelding.objects.filter(arrangementid = arrangements['arrangementid'])
            available = arrangements['antallplasser'] - len(guests)
            available_dict.update({arrangements['arrangementid']: available})

    else:
        return redirect("/")

    return render(request, 'mealOverview.html', {"object_list" : queryset, 'available_dict': available_dict, 'site_logged_in' : is_logged_in(request)})

def chooseMeal(request, arrangementid):
    if is_logged_in(request):
        dinner = Arrangement.objects.get(arrangementid = arrangementid)
        guests = Pamelding.objects.filter(arrangementid = arrangementid)
        number_guests = len(guests)
        available = dinner.antallplasser - number_guests

        try:
            in_dinner = Pamelding.objects.get(brukerid=request.session['user_id_logged_in'], arrangementid = arrangementid)
            is_in_dinner = True
        except:
            is_in_dinner = False
        try:
            owner = Vertskap.objects.get(brukerid = request.session['user_id_logged_in'], arrangementid = arrangementid)
            is_owner = True

        except:
            is_owner = False

        if request.POST:

            if ('book_dinner' in request.POST):
                if(is_in_dinner):
                    in_dinner.delete()
                    return redirect("../../oversikt/")
                else:
                    in_dinner = Pamelding(brukerid = request.session['user_id_logged_in'], arrangementid = arrangementid, tidspunkt = timezone.now())
                    in_dinner.save()
                    return redirect("../../oversikt/")
            #elif ('edit_dinner' in request.POST):

            elif ('cancel_dinner' in request.POST):
                print("cancel")


    else:
        return redirect("/")

    return render(request, 'chooseMeal.html', {'dinner': dinner, 'is_in_dinner': is_in_dinner, 'is_owner':is_owner, 'number_guests': number_guests, 'available': available ,'site_logged_in': is_logged_in(request)})

def editMeal(request, arrangementid):
    if is_logged_in(request):
        dinner = Arrangement.objects.get(arrangementid = arrangementid)
        time_stamp = str(dinner.tidspunkt)
        time_stamp  = time_stamp.split(" ")

        date = time_stamp[0]
        time = time_stamp[1]


        if request.POST:
            arrangement_name = request.POST.get('arrangement_name')
            description = request.POST.get('description')
            seats = request.POST.get('seats')
            location = request.POST.get('location')
            time = request.POST.get('time')
            prize = request.POST.get('prize')
            date = request.POST.get('date')

            datetime = date + " " + time


            dinner.arrangementnavn = arrangement_name
            dinner.beskrivelse = description
            dinner.antallplasser = seats
            dinner.lokasjon = location
            dinner.tidspunkt = datetime
            dinner.pris = prize


            dinner.save()
            return redirect('../../../')

    else:
        return redirect('/')
    return render(request, 'editMeal.html', {'dinner':dinner, 'date':date, 'time':time, 'site_logged_in': is_logged_in(request)})