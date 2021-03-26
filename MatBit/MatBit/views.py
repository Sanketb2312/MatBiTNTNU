from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from .mymodels import User, UserAllergy, DinnerEvent, EventIngredient, Ingredient, Registration, Host
from django.utils import timezone
from datetime import datetime
import re


# Model.objects is set with setattr(__o, __name, __value) in django/db/models/base.py;
# commonly known as an anti-pattern. The type is: django/db/models/manager.py:Manager, which so usefully is empty.
# HttpRequest.session is set by the session middleware; also an anti-pattern.

def is_logged_in(request: HttpRequest) -> bool:
    return 'user_id_logged_in' in request.session

def is_admininistrator(request: HttpRequest) -> bool:
    if request.session['admin_token'] == 1:
        return True
    elif request.session['admin_token'] == 0:
        return False

def frontpage(request: HttpRequest) -> HttpResponse:
    return render(request, 'frontpage.html', {'site_logged_in': is_logged_in(request)})


# TODO: move to another file
# TODO: should send e-mail with validation token
def add_user(
        first_name: str,
        last_name: str,
        birth_date: str,
        address: str,
        post_code: str,
        location: str,
        is_admin: bool,
        email: str,
        password: str
):

    if len(email) < 3:
        raise ValidationError("Invalid e-mail")

    for i in range(1, len(email) - 2):
        if email[i] == "@":
            break
    else:
        raise ValidationError("Invalid e-mail")

    birth_date_components = birth_date.split("-")

    if len(birth_date_components) != 3 \
            or len(birth_date_components[0]) != 4 \
            or len(birth_date_components[1]) != 2 \
            or len(birth_date_components[2]) != 2:
        raise ValidationError("Invalid birth date format")

    try:
        birth_date_components = tuple(map(int, birth_date_components))
    except ValueError:
        raise ValidationError("Invalid birth date format")

    today = datetime.today()
    max_date_components = (today.year - 15, today.month, today.day)

    if birth_date_components[0] > max_date_components[0] or (birth_date_components[0] == max_date_components[0] and
       (birth_date_components[1] > max_date_components[1] or (birth_date_components[1] == max_date_components[1] and
        (birth_date_components[2] > max_date_components[2])))
    ):
        raise ValidationError(
            "This person is too young to use this service; birth date: " + str(birth_date_components) +
            "; latest allowed birth date: " + str(max_date_components)
        )

    try:
        user = User(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            address=address,
            post_code=post_code,
            location=location,
            is_admin="1" if is_admin else "0",
            email=email,
            password=password
        )
    except ValueError:
        # Thrown if post_code is not a number
        raise ValidationError("post_code is not a number")
    else:
        user.save()


def register(request: HttpRequest) -> HttpResponse:
    # FIXME: shouldn't there be a check for logged in?

    invalid_form_data = False

    email_used = False
    first_name = None
    last_name = None
    birth_date = None
    address = None
    post_code = None
    location = None

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
            try:
                add_user(
                    first_name=first_name,
                    last_name=last_name,
                    birth_date=birth_date,
                    address=address,
                    post_code=post_code,
                    location=location,
                    is_admin=False,
                    email=email,
                    password=password
                )
            except ValidationError:
                invalid_form_data = True
            else:
                return redirect('/')

    return render(request, "registerUser.html", {
        "properties": {
            'invalidFormData': invalid_form_data,
            'emailUsed': email_used,
            'first_name': first_name,
            'last_name': last_name,
            'birth_date': birth_date,
            'address': address,
            'post_code': post_code,
            'location': location,
            'site_logged_in': is_logged_in(request)  # FIXME: see fixme above.
        }
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
            request.session['admin_token'] = user.is_admin

            return redirect('/')

    return render(request, 'login.html', {
        'error_login': error_login,
        'site_logged_in': is_logged_in(request)
    })


def logout(request: HttpRequest) -> HttpResponse:
    if is_logged_in(request):
        del request.session['user_id_logged_in']
        del request.session['admin_token']

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
        'admin_user': is_admininistrator(request),
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

        maxAllergiID = Ingredient.ingredients.all().last().ingredient_id
        for x in range(0, maxAllergiID+1):
            print(request.POST)
            print(meal.event_id)
            if str(x) in request.POST:
                print(11111)
                event_ingredient = EventIngredient(event_id = meal.event_id, ingredient_id = x)
                event_ingredient.save()



        # noinspection SpellCheckingInspection
        return redirect('../../profil/')

    allergener = Ingredient.ingredients.all()


    return render(request, 'newMeal.html', {'allergener':allergener,'site_logged_in': is_logged_in(request)})


# noinspection SpellCheckingInspection
def meal_overview(request: HttpRequest) -> HttpResponse:
    if not is_logged_in(request):
        return redirect("/")

    available_dict = {}

    queryset = DinnerEvent.events.all()

    future_events_dict = {}


    # Gives the number of guests already booked for this dinner
    for event in queryset:

        event_id = event.event_id

        guests = Registration.registrations.filter(event_id=event_id)
        available = event.capacity - len(guests)
        available_dict[event_id] = available

    # Checks if the event is in the future, or has passed.
        if event.date > datetime.today():
            future_events_dict[event_id] = event


    return render(request, 'mealOverview.html', {
        "object_list": queryset,
        'available_dict': available_dict,
        'site_logged_in': is_logged_in(request),
        'future_events_dict': future_events_dict
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

    dinner = DinnerEvent.events.get(event_id=event_id)
    guests = Registration.registrations.filter(event_id=event_id)
    guest_count = len(guests)
    available = dinner.capacity - guest_count
    price = dinner.cost

    if guest_count == 0:
        guest_price = price
    else:
        guest_price = round(price / guest_count)

    in_dinner = get_in_dinner(request, event_id)
    signed_up = in_dinner is not None
    try:
        owner = Host.hosts.get(user_id=request.session['user_id_logged_in'], event_id=event_id)
        is_owner = True

    except:
        is_owner = False
    if request.POST:
        if ('book_dinner' in request.POST):
            if signed_up:
                in_dinner.delete()
            else:
                in_dinner = Registration(
                    user_id=request.session['user_id_logged_in'],
                    event_id=event_id,
                    date=timezone.now()
                )
                in_dinner.save()
        elif ('cancel_dinner' in request.POST):
            dinner.is_cancelled = 1
            dinner.save()
        # noinspection SpellCheckingInspection
        return redirect("../../oversikt/")


    allergiesInDinner = []
    for allergy in EventIngredient.event_ingredients.all():
        if allergy.event_id == event_id:
            allergiesInDinner.append(allergy.ingredient_id)

    counter = 0
    if not len(allergiesInDinner) == 0:
        for x in Ingredient.ingredients.all():
            if allergiesInDinner[counter] == x.ingredient_id:
                allergiesInDinner[counter] = x.name
                if counter == len(allergiesInDinner)-1:
                    break
                counter+=1



    return render(request, 'chooseMeal.html', {
        'dinner': dinner,
        'in_dinner': in_dinner,
        'is_owner': is_owner,
        'guest_count': guest_count,
        'guest_price': guest_price,
        'available': available,
        'allergiesInDinner': allergiesInDinner,
        'checkLen': len(allergiesInDinner) == 0,
        'admin_user': has_admin_privileges(request),
        'site_logged_in': is_logged_in(request)
    })


def edit_meal(request: HttpRequest, event_id: int) -> HttpResponse:
    if not is_logged_in(request):
        return redirect('/')
    dinner = DinnerEvent.events.get(event_id = event_id)
    time_stamp = str(dinner.date)
    time_stamp  = time_stamp.split(" ")

    day = time_stamp[0]
    time = time_stamp[1]


    if request.POST:
        arrangement_name = request.POST.get('arrangement_name')
        description = request.POST.get('description')
        seats = request.POST.get('seats')
        location = request.POST.get('location')
        time = request.POST.get('time')
        prize = request.POST.get('prize')
        day = request.POST.get('date')

        datetime = day + " " + time


        dinner.name = arrangement_name
        dinner.description = description
        dinner.capacity = seats
        dinner.location = location
        dinner.date = datetime
        dinner.cost = prize


        dinner.save()
        return redirect('../../../')

    return render(request, 'editMeal.html', {
        'dinner':dinner,
        'date':day,
        'time':time,
        'site_logged_in': is_logged_in(request)})


def add_allergies(request: HttpRequest) -> HttpResponse:
    if not is_logged_in(request):
        return redirect('/')

    allergiesListWithID = []
    allergiesList=[]
    for i in UserAllergy.users_allergies.all(): #Change to .filter() to get immediate all with user_id
        if i.user_id == request.session['user_id_logged_in']:
            allergiesListWithID.append(i.ingredient_id)

    for x in range(0, len(allergiesListWithID)):
        allergiesList.append(Ingredient.ingredients.get(ingredient_id = allergiesListWithID[x]).name)
    print(allergiesListWithID)
    allergens = Ingredient.ingredients.all()
    maxAllergyID = allergens.last().ingredient_id

    if request.POST:
        for x in range (0,maxAllergyID+1):
            if str(x) in request.POST:
                if x not in allergiesListWithID:
                    allergy = UserAllergy(user_id = request.session['user_id_logged_in'], ingredient_id = x)
                    allergy.save()
            else:
                #print(allergiesListWithID, "heieiei")
                if x in allergiesListWithID:
                    allergy = UserAllergy.users_allergies.get(user_id = request.session['user_id_logged_in'], ingredient_id = x)
                    allergy.delete()



        return redirect("../../profil")


    return render(request, 'addAllergies.html', {
        'object_list': allergens,
        'allergiesList': allergiesList,
        'site_logged_in' : is_logged_in(request)})
