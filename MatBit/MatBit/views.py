from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from .mymodels import User, UserAllergy, DinnerEvent, EventIngredient, Ingredient, Registration, Host
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
        location = request.POST.get('location')

        try:
            User.users.get(email=email)
            email_used = True

        except ObjectDoesNotExist:
            user = User(
                first_name=first_name,
                last_name=last_name,
                birth_date=birth_date,
                address=address,
                post_code=post_code,
                location=location,
                is_admin="0",
                email=email,
                password=password
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
            user = User.users.get(email=email, password=password)
        except ObjectDoesNotExist:
            error_login = True
        else:
            request.session['user_id_logged_in'] = user.user_id

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

    user = User.users.get(user_id=request.session['user_id_logged_in'])

    # Linking all the allergies in the database that the user has.
    allergies = UserAllergy.users_allergies.filter(user_id=request.session['user_id_logged_in']).all()

    for allergy in allergies:

        ingredient = Ingredient.ingredients.get(ingredient_id=allergy.ingredient_id)
        allergy_dict[ingredient.ingredient_id] = ingredient.name

    # Collecting all the registrations the user has made.
    registrations = Registration.registrations.filter(user_id=request.session['user_id_logged_in']).all()

    for registration in registrations:

        dinner_information = DinnerEvent.events.get(event_id=registration.event_id)

        event_dict[dinner_information.event_id] = [
            dinner_information.name,
            dinner_information.location,
            dinner_information.date
        ]

    # Collecting all the events the user is hosting.
    hosting = Host.hosts.filter(user_id=request.session['user_id_logged_in']).all()

    for hosting_event in hosting:

        hosting_information = DinnerEvent.events.get(event_id=hosting_event.event_id)

        hosting_dict[hosting_information.event_id] = [
            hosting_information.name,
            hosting_information.date,
            hosting_information.capacity
        ]

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

    user = User.users.get(user_id=request.session['user_id_logged_in'])

    if request.POST:
        # FIXME: Why are these queried like this, instead of just using: user.<> = request.POST.get('<>')?
        #  In case one of them throws an error, nothing is updated?
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        post_code = request.POST.get('post_code')
        place = request.POST.get('location')

        user.first_name = first_name
        user.last_name = last_name
        user.address = address
        user.post_code = post_code
        user.location = place
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
        event_name = request.POST.get('dinner_name')
        description = request.POST.get('description')
        capacity = request.POST.get('seats')
        location = request.POST.get('location')
        date = request.POST.get('date')
        time = request.POST.get('time')
        cost = request.POST.get('cost')

        datetime = date + " " + time + ":00"

        meal = DinnerEvent(
            name=event_name,
            description=description,
            capacity=capacity,
            location=location,
            date=datetime,
            creation_date=timezone.now(),
            cost=cost,
            is_cancelled=0
        )

        meal.save()

        host = Host(user_id=request.session['user_id_logged_in'], event_id=meal.event_id)
        host.save()

        # noinspection SpellCheckingInspection
        return redirect('../../profil/')

    return render(request, 'newMeal.html', {'site_logged_in': is_logged_in(request)})


# noinspection SpellCheckingInspection
def meal_overview(request: HttpRequest) -> HttpResponse:
    if not is_logged_in(request):
        return redirect("/")

    available_dict = {}

    queryset = DinnerEvent.events.all()

    # Gives the number of guests already booked for this dinner
    for event in queryset:

        event_id = event.event_id

        guests = Registration.registrations.filter(event_id=event_id)
        available = event.capacity - len(guests)
        available_dict[event_id] = available

    return render(request, 'mealOverview.html', {
        "object_list": queryset,
        'available_dict': available_dict,
        'site_logged_in': is_logged_in(request)
    })


def get_in_dinner(request: HttpRequest, event_id: int) -> Registration or None:
    try:
        return Registration.registrations.get(user_id=request.session['user_id_logged_in'], event_id=event_id)
    except ObjectDoesNotExist:  # Could've used Registration.DoesNotExist, but this saves us a warning suppression.
        return None


def choose_meal(request: HttpRequest, event_id: int) -> HttpResponse:
    event_id = event_id

    if not is_logged_in(request):
        return redirect("/")

    in_dinner = get_in_dinner(request, event_id)
    signed_up = in_dinner is not None

    if request.POST:
        if signed_up:
            in_dinner.delete()
        else:
            in_dinner = Registration(
                user_id=request.session['user_id_logged_in'],
                event_id=event_id,
                date=timezone.now()
            )
            in_dinner.save()

        # noinspection SpellCheckingInspection
        return redirect("../../oversikt/")

    dinner = DinnerEvent.events.get(event_id=event_id)
    guests = Registration.registrations.filter(event_id=event_id)

    guest_count = len(guests)
    available = dinner.capacity - guest_count

    return render(request, 'chooseMeal.html', {
        'dinner': dinner,
        'is_in_dinner': signed_up,
        'number_guests': guest_count,
        'available': available,
        'site_logged_in': is_logged_in(request)
    })

def addAllergies(request):
    if is_logged_in(request):
        allergiesListWithID = []
        allergiesList=[]
        for i in Harallergi.objects.all():
            if i.brukerid == request.session['user_id_logged_in']:
                allergiesListWithID.append(i.innholdid)

        for x in range(0, len(allergiesListWithID)):
            allergiesList.append(Innhold.objects.get(innholdid = allergiesListWithID[x]).navn)
        print(allergiesListWithID)
        allergener = Innhold.objects.all()
        maxAllergiID = allergener.last().innholdid

        if request.POST:
            for x in range (0,maxAllergiID+1):
                if str(x) in request.POST:
                    if x not in allergiesListWithID:
                        allergi = Harallergi(brukerid = request.session['user_id_logged_in'], innholdid = x)
                        allergi.save()
                else:
                    print(allergiesListWithID, "heieiei")
                    if x in allergiesListWithID:
                        allergi = Harallergi.objects.get(brukerid = request.session['user_id_logged_in'], innholdid = x)
                        allergi.delete()



            return redirect("../../profil")
    return render(request, 'addallergies.html', {'object_list':allergener, 'site_logged_in' : is_logged_in(request), 'allergiesList': allergiesList})
