from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from .mymodels import Bruker, Harallergi, Arrangement, Arrangementinnhold, Innhold, Pamelding, Vertskap
from django.utils import timezone


# Model.objects is set with setattr(__o, __name, __value) in django/db/models/base.py;
# commonly known as an anti-pattern. The type is: django/db/models/manager.py:Manager, which so usefully is empty.
# HttpRequest.session is set by the session middleware; also an anti-pattern.

def is_logged_in(request: HttpRequest) -> bool:
    return 'user_id_logged_in' in request.session


def frontpage(request: HttpRequest) -> HttpResponse:
    return render(request, 'frontpage.html', {'site_logged_in': is_logged_in(request)})


def register(request: HttpRequest) -> HttpResponse:
    # FIXME: shouldn't there be a check for logged in?

    email_used = False
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
            Bruker.users.get(epost=email)
            email_used = True

        except ObjectDoesNotExist:
            user = Bruker(
                fornavn=first_name,
                etternavn=last_name,
                fodselsdato=birth_date,
                adresse=address,
                postnummer=post_code,
                sted=place,
                eradministrator="0",
                epost=email,
                passord=password
            )
            user.save()

            return redirect('/')

    return render(request, "registerUser.html", {
        'emailUsed': email_used,
        'first_name': first_name,
        'last_name': last_name,
        'birth_date': birth_date,
        'address': address,
        'post_code': post_code,
        'place': place,
        'site_logged_in': is_logged_in(request)  # FIXME: see fixme above.
    })


def login(request: HttpRequest) -> HttpResponse:
    if is_logged_in(request):
        return redirect('/')

    error_login = False

    if request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Bruker.users.get(epost=email, passord=password)
        except ObjectDoesNotExist:
            error_login = True
        else:
            request.session['user_id_logged_in'] = user.brukerid

            return redirect('/')

    return render(request, 'login.html', {
        'error_login': error_login,
        'site_logged_in': is_logged_in(request)
    })


def logout(request: HttpRequest) -> HttpResponse:
    if is_logged_in(request):
        del request.session['user_id_logged_in']

    return redirect('/')


# noinspection SpellCheckingInspection
def profile(request: HttpRequest) -> HttpResponse:
    if not is_logged_in(request):
        return redirect('/')

    allergy_dict = {}
    hosting_dict = {}
    event_dict = {}

    user = Bruker.users.get(brukerid=request.session['user_id_logged_in'])

    allergy = Harallergi.objects.filter(brukerid=request.session['user_id_logged_in'])
    # allergy = {'allergi' : allergy}

    for allergies in allergy:
        allergies = allergies.__dict__  # FIXME: unnecessary, right?

        content = Innhold.objects.get(innholdid=allergies['innholdid'])
        allergy_dict.update({content.innholdid: content.navn})

    # TODO: rename to "event"/"events" or something.
    arrangement = Pamelding.objects.filter(brukerid=request.session['user_id_logged_in'])

    for arrangements in arrangement:
        arrangements = arrangements.__dict__  # FIXME: unnecessary, right?

        dinner_information = Arrangement.events.get(arrangementid=arrangements['arrangementid'])

        event_dict.update({dinner_information.arrangementid: [
            dinner_information.arrangementnavn,
            dinner_information.lokasjon,
            dinner_information.tidspunkt
        ]})

    hosting = Vertskap.objects.filter(brukerid=request.session['user_id_logged_in'])

    for hosting_event in hosting:
        hosting_event = hosting_event.__dict__  # FIXME: unnecessary, right?

        hosting_information = Arrangement.events.get(arrangementid=hosting_event['arrangementid'])

        hosting_dict.update({hosting_information.arrangementid: [
            hosting_information.arrangementnavn,
            hosting_information.tidspunkt,
            hosting_information.antallplasser
        ]})

    return render(request, 'profile.html', {
        'user': user,
        'userAllergies': allergy_dict,
        'arrangement': event_dict,
        'hosting': hosting_dict,
        'site_logged_in': is_logged_in(request)
    })


def edit_user(request: HttpRequest) -> HttpResponse:
    if not is_logged_in(request):
        return redirect('/')

    user = Bruker.users.get(brukerid=request.session['user_id_logged_in'])

    if request.POST:
        # FIXME: Why are these queried like this, instead of just using: user.<> = request.POST.get('<>')?
        #  In case one of them throws an error?
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

        # noinspection SpellCheckingInspection
        return redirect('../../profil/')

    return render(request, 'editUser.html', {
        'user': user,
        'site_logged_in': is_logged_in(request)
    })


def new_meal(request: HttpRequest) -> HttpResponse:
    if not is_logged_in(request):
        return redirect("/")

    if request.POST:
        # FIXME: see fixme in edit_user(_:)
        arrangement_name = request.POST.get('arrangement_name')
        description = request.POST.get('description')
        seats = request.POST.get('seats')
        location = request.POST.get('location')
        date = request.POST.get('date')
        time = request.POST.get('time')
        prize = request.POST.get('prize')

        datetime = date + " " + time + ":00"

        meal = Arrangement(
            arrangementnavn=arrangement_name,
            beskrivelse=description,
            antallplasser=seats,
            lokasjon=location,
            tidspunkt=datetime,
            opprettet=timezone.now(),
            pris=prize,
            avlyst=0
        )

        meal.save()

        host = Vertskap(brukerid=request.session['user_id_logged_in'], arrangementid=meal.arrangementid)
        host.save()

        # noinspection SpellCheckingInspection
        return redirect('../../profil/')

    return render(request, 'newMeal.html', {'site_logged_in': is_logged_in(request)})


# noinspection SpellCheckingInspection
def meal_overview(request: HttpRequest) -> HttpResponse:
    if not is_logged_in(request):
        return redirect("/")

    available_dict = {}

    queryset = Arrangement.events.all()

    # Gives the number of guests already booked for this dinner
    # FIXME: "arrangements"???
    for arrangements in queryset:
        arrangements = arrangements.__dict__  # FIXME: unnecessary, right?
        guests = Pamelding.objects.filter(arrangementid=arrangements['arrangementid'])
        available = arrangements['antallplasser'] - len(guests)
        available_dict.update({arrangements['arrangementid']: available})

    return render(request, 'mealOverview.html', {
        "object_list": queryset,
        'available_dict': available_dict,
        'site_logged_in': is_logged_in(request)
    })


def get_in_dinner(request: HttpRequest, event_id: int) -> Pamelding or None:
    try:
        return Pamelding.objects.get(brukerid=request.session['user_id_logged_in'], arrangementid=event_id)
    except ObjectDoesNotExist:  # Could've used Pamelding.DoesNotExist, but this saves us a warning suppression.
        return None


# TODO: rename the second argument. Also renaming the argument in urls.py fixes signing up,
#  but retracting the signup still crashes.
def choose_meal(request: HttpRequest, arrangementid: int) -> HttpResponse:
    event_id = arrangementid

    if not is_logged_in(request):
        return redirect("/")

    in_dinner = get_in_dinner(request, event_id)
    signed_up = in_dinner is not None

    if request.POST:
        if signed_up:
            in_dinner.delete()
        else:
            in_dinner = Pamelding(
                brukerid=request.session['user_id_logged_in'],
                arrangementid=event_id,
                tidspunkt=timezone.now()
            )
            in_dinner.save()

        # noinspection SpellCheckingInspection
        return redirect("../../oversikt/")

    dinner = Arrangement.events.get(arrangementid=event_id)
    guests = Pamelding.objects.filter(arrangementid=event_id)

    guest_count = len(guests)
    available = dinner.antallplasser - guest_count

    return render(request, 'chooseMeal.html', {
        'dinner': dinner,
        'is_in_dinner': signed_up,
        'number_guests': guest_count,
        'available': available,
        'site_logged_in': is_logged_in(request)
    })
