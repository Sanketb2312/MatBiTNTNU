from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect

from .database_access import is_logged_in, has_admin_privileges, add_user, get_in_dinner, create_dinner, delete_user, \
    cancel_dinner
from .mymodels import User, UserAllergy, DinnerEvent, EventIngredient, Ingredient, Registration, Host, Feedback
from django.utils import timezone
from datetime import datetime

from django.contrib.auth.hashers import check_password, make_password


# Model.objects is set with setattr(__o, __name, __value) in django/db/models/base.py;
# commonly known as an anti-pattern. The type is: django/db/models/manager.py:Manager, which so usefully is empty.
# HttpRequest.session is set by the session middleware; also an anti-pattern.

def render_page(request: HttpRequest, document: str, arguments: {str: object} or None = None) -> HttpResponse:
    if arguments is None:
        arguments = {}

    return render(request, document, arguments | {
        "site_logged_in": is_logged_in(request),
        "is_admin": has_admin_privileges(request)
    })


def frontpage(request: HttpRequest) -> HttpResponse:
    return render_page(request, 'frontpage.html')


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

    return render_page(request, "registerUser.html", {
        "properties": {
            'invalidFormData': invalid_form_data,
            'emailUsed': email_used,
            'first_name': first_name,
            'last_name': last_name,
            'birth_date': birth_date,
            'address': address,
            'post_code': post_code,
            'location': location
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
            print(password)
            user = User.users.get(email=email)
            #Used this to create a new hashed password
            print(make_password(password))
            if not check_password(password, user.password):
                raise ObjectDoesNotExist

        except ObjectDoesNotExist:
            error_login = True
        else:
            request.session['user_id_logged_in'] = user.user_id
            request.session['admin_token'] = user.is_admin

            return redirect('/')

    return render_page(request, 'login.html', {
        'error_login': error_login
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
    past_event_dict = {}
    event_ids = []

    user_id = request.session['user_id_logged_in']

    user = User.users.get(user_id=user_id)

    # Linking all the allergies in the database that the user has.
    allergies = UserAllergy.users_allergies.filter(user_id=user_id).all()

    for allergy in allergies:

        ingredient = Ingredient.ingredients.get(ingredient_id=allergy.ingredient_id)
        allergy_dict[ingredient.ingredient_id] = ingredient.name

    # Collecting all the registrations the user has made.
    registrations = Registration.registrations.filter(user_id=user_id).all()

    for registration in registrations:

        dinner_information = DinnerEvent.events.get(event_id=registration.event_id)

        event_dict[dinner_information.event_id] = [
            dinner_information.name,
            dinner_information.location,
            dinner_information.date
        ]

        if dinner_information.date < datetime.today():
            event_ids.append(dinner_information.event_id)
            past_event_dict[dinner_information.event_id] = [
            dinner_information.name,
            dinner_information.location,
            dinner_information.date
        ]

    # Collecting all the events the user is hosting.
    hosting = Host.hosts.filter(user_id=user_id).all()

    for hosting_event in hosting:

        hosting_information = DinnerEvent.events.get(event_id=hosting_event.event_id)

        hosting_dict[hosting_information.event_id] = [
            hosting_information.name,
            hosting_information.date,
            hosting_information.capacity
        ]

    feedback = Feedback.feedbacks.filter(user_id_host=request.session['user_id_logged_in'])

    feedback_dict = {}
    user_comment = None
    feedback_event = None

    for feed in feedback:
        user_comment = feed.user_id_comment
        feedback_event = feed.event_id

        feedback_event_name = DinnerEvent.events.filter(event_id=feedback_event)
        user_comment_name = User.users.filter(user_id=user_comment)
        feedback_dict[feed.feedbackid] = [
            feedback_event_name, user_comment_name, feed.comment, feed.rating
        ]
    print(feedback_dict)

    for key, value in feedback_dict.items():
        for event in value[0]:
            value[0] = event.name
        for user_name in value[1]:
            value[1] = user_name.first_name + " " + user_name.last_name

    return render_page(request, 'profile.html', {
        'user': user,
        'userAllergies': allergy_dict,
        'arrangement': event_dict,
        'hosting': hosting_dict,
        'admin_user': has_admin_privileges(request),  # FIXME: unnecessary. Needs to switch to "is_admin" in the HTML.
        'past_event_dict': past_event_dict,
        'event_ids': event_ids,
        'feedback': feedback,
        'feedback_dict': feedback_dict
    })


def edit_user(request: HttpRequest) -> HttpResponse:
    if not is_logged_in(request):
        return redirect('/')

    user = User.users.get(user_id=request.session['user_id_logged_in'])

    if request.POST:
        if "edit" in request.POST:
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
        elif "delete" in request.POST:
            delete_user(user)

            return logout(request)

    return render_page(request, 'editUser.html', {
        'user': user
    })


# FIXME: please welcome one of the most inefficient functions in existence.
def profiles_list(request: HttpRequest) -> HttpResponse:
    if not (is_logged_in(request) and has_admin_privileges(request)):
        return redirect("/")

    accounts = User.users.all()

    return render_page(request, 'profilesList.html', {
        "accounts": accounts
    })


def new_meal(request: HttpRequest) -> HttpResponse:
    if not is_logged_in(request):
        return redirect("/")

    if request.POST:
        # FIXME: see fixme in edit_user(_:)
        meal = create_dinner(
            request.POST.get('dinner_name'),
            request.POST.get('description'),
            request.POST.get('seats'),
            request.POST.get('location'),
            request.POST.get('date'),
            request.POST.get('time'),
            request.POST.get('cost')
        )

        host = Host(user_id=request.session['user_id_logged_in'], event_id=meal.event_id)
        host.save()

        max_allergy_id = Ingredient.ingredients.all().last().ingredient_id

        for allergy_id in range(max_allergy_id + 1):
            #print(request.POST)
            #print(meal.event_id)

            if str(allergy_id) in request.POST:

                EventIngredient(event_id=meal.event_id, ingredient_id=allergy_id).save()

        # noinspection SpellCheckingInspection
        return redirect('../../profil/')

    allergens = Ingredient.ingredients.all()

    return render_page(request, 'newMeal.html', {'allergens': allergens})


# noinspection SpellCheckingInspection
def meal_overview(request: HttpRequest) -> HttpResponse:
    if not is_logged_in(request):
        return redirect("/")

    available_dict = {}

    queryset = DinnerEvent.events.filter(date__gte = datetime.today())  #Gets the objects from database with datetime after now
    queryset = queryset.order_by('date')    #Sorts the input by date

    #Adds event ids in a array for use in filtration
    event_ids = []
    for id in queryset:
        event_ids.append(id.event_id)

    # Gives the number of guests already booked for this dinner
    for event in queryset:
        event_id = event.event_id

        guests = Registration.registrations.filter(event_id=event_id)
        available = event.capacity - guests.count()
        available_dict[event_id] = available

    #Creates an array for filtration with locations on the webpage
    locations = []
    event_location = {}
    for dinner_place in queryset:
        if dinner_place.event_id not in event_location:
            event_location[dinner_place.event_id] = dinner_place.location.lower()
        if dinner_place.location.lower() not in locations:
            locations.append(dinner_place.location.lower())

    #Creates an array for filtration with allergies on the webpage
    events_allergy = {}
    for event in queryset:
        query = EventIngredient.event_ingredients.filter(event_id=event.event_id)
        for x in query:
            if x.event_id not in events_allergy:
                events_allergy[x.event_id] = []
            events_allergy[x.event_id].append(x.ingredient_id)

    return render_page(request, 'mealOverview.html', {
        "object_list": queryset,
        'available_dict': available_dict,
        'allergies':Ingredient.ingredients.all(),
        'locations' : locations,
        'event_location' : event_location,
        'events_allergy' : events_allergy,
        'event_ids':event_ids
    })


def choose_meal(request: HttpRequest, event_id: int) -> HttpResponse:

    event_id = event_id

    if not is_logged_in(request):
        return redirect("/")

    dinner = DinnerEvent.events.get(event_id=event_id)
    guests = Registration.registrations.filter(event_id=event_id)
    guest_count = guests.count()
    available = dinner.capacity - guest_count

    if guest_count == 0:
        guest_price = dinner.cost
    else:
        guest_price = round(dinner.cost / guest_count)

    in_dinner = get_in_dinner(request, event_id)
    signed_up = in_dinner is not None
    is_owner = Host.hosts.filter(user_id=request.session['user_id_logged_in'], event_id=event_id).exists()
    # TODO: legg til navn på verten i brukergrensesnittet. Hvis verten ikke eksisterer, er den kontoen slettet.
    #  I så fall skal middagen være avlyst. Hvis den ikke er det, har vi en intern feil.

    if request.POST:
        if 'book_dinner' in request.POST:
            if signed_up:
                in_dinner.delete()
            else:
                in_dinner = Registration(
                    user_id=request.session['user_id_logged_in'],
                    event_id=event_id,
                    date=timezone.now()
                )
                in_dinner.save()
        elif 'cancel_dinner' in request.POST:
            cancel_dinner(dinner)

        # noinspection SpellCheckingInspection
        return redirect("../../oversikt/")

    allergies_in_dinner = []
    for allergy in EventIngredient.event_ingredients.all():
        if allergy.event_id == event_id:
            allergies_in_dinner.append(allergy.ingredient_id)

    counter = 0
    if not len(allergies_in_dinner) == 0:
        allergies_in_dinner.sort()
        for ingredient in Ingredient.ingredients.all():
            if allergies_in_dinner[counter] == ingredient.ingredient_id:
                allergies_in_dinner[counter] = ingredient.name

                if counter >= len(allergies_in_dinner) - 1:
                    break

                counter += 1

    return render_page(request, 'chooseMeal.html', {
        'dinner': dinner,
        'in_dinner': in_dinner,
        'is_owner': is_owner,
        'guest_count': guest_count,
        'guest_price': guest_price,
        'available': available,
        'allergiesInDinner': allergies_in_dinner,
        'checkLen': len(allergies_in_dinner) == 0,
        'admin_user': has_admin_privileges(request)  # FIXME: unnecessary. Needs to switch to "is_admin" in the HTML.
    })


def edit_meal(request: HttpRequest, event_id: int) -> HttpResponse:
    if not is_logged_in(request):
        return redirect('/')
    dinner = DinnerEvent.events.get(event_id=event_id)
    time_stamp = str(dinner.date)
    time_stamp = time_stamp.split(" ")

    day = time_stamp[0]
    time = time_stamp[1]

    event_ingredients = EventIngredient.event_ingredients.filter(event_id=dinner.event_id)

    event_ingredients_name = []
    event_ingredients_ids = []
    for ingredients in event_ingredients:
        for ingredient_id in Ingredient.ingredients.all():
            if ingredients.ingredient_id == ingredient_id.ingredient_id:
                event_ingredients_name.append(ingredient_id.name)
                event_ingredients_ids.append(ingredient_id.ingredient_id)

    if request.POST:
        arrangement_name = request.POST.get('arrangement_name')
        description = request.POST.get('description')
        seats = request.POST.get('seats')
        location = request.POST.get('location')
        time = request.POST.get('time')
        prize = request.POST.get('prize')
        day = request.POST.get('date')

        date_and_time = day + " " + time

        dinner.name = arrangement_name
        dinner.description = description
        dinner.capacity = seats
        dinner.location = location
        dinner.date = date_and_time
        dinner.cost = prize

        max_allergy_id = Ingredient.ingredients.all().last().ingredient_id

        for allergy_id in range(max_allergy_id + 1):
            if str(allergy_id) in request.POST:
                if allergy_id not in event_ingredients_ids:
                    EventIngredient(event_id=event_id, ingredient_id=allergy_id).save()
            else:
                if allergy_id in event_ingredients_ids:

                    allergy = EventIngredient.event_ingredients.get(event_id=dinner.event_id, ingredient_id=allergy_id)
                    print(allergy)
                    allergy.delete()

        dinner.save()

        return redirect('../../../')

    return render_page(request, 'editMeal.html', {
        'dinner': dinner,
        'date': day,
        'time': time,
        'allergens': Ingredient.ingredients.all(),
        'event_ingredients_name': event_ingredients_name
    })


def add_allergies(request: HttpRequest) -> HttpResponse:
    if not is_logged_in(request):
        return redirect('/')

    allergies_list_with_id = []
    allergies_list = []

    for i in UserAllergy.users_allergies.all():  # Change to .filter() to get immediate all with user_id
        if i.user_id == request.session['user_id_logged_in']:
            allergies_list_with_id.append(i.ingredient_id)

    for x in range(0, len(allergies_list_with_id)):
        allergies_list.append(Ingredient.ingredients.get(ingredient_id=allergies_list_with_id[x]).name)
    #print(allergies_list_with_id)
    allergens = Ingredient.ingredients.all()
    max_allergy_id = allergens.last().ingredient_id

    if request.POST:
        for x in range(0, max_allergy_id + 1):
            if str(x) in request.POST:
                if x not in allergies_list_with_id:
                    allergy = UserAllergy(user_id=request.session['user_id_logged_in'], ingredient_id=x)
                    allergy.save()
            else:
                # print(allergies_list_with_id, "heieiei")
                if x in allergies_list_with_id:
                    allergy = UserAllergy.users_allergies.get(
                        user_id=request.session['user_id_logged_in'],
                        ingredient_id=x
                    )
                    allergy.delete()

        # noinspection SpellCheckingInspection
        return redirect("../../profil")

    return render_page(request, 'addAllergies.html', {
        'object_list': allergens,
        'allergiesList': allergies_list
    })

def feedback(request : HttpRequest, event_id: int) -> HttpResponse:
    if not is_logged_in(request):
        return redirect('/')

    event_id = event_id
    user_host = Host.hosts.filter(event_id=event_id)

    for user in user_host:
        user_host=user.user_id

    check_existing_feedback = False
    feedback = Feedback.feedbacks.filter(user_id_comment = request.session['user_id_logged_in'])

    for feed in feedback:
        if user_host == feed.user_id_host and feed.event_id == event_id:
            check_existing_feedback = True

    if request.POST:
        comment = request.POST.get("comment")
        rating = request.POST.get("rate")
        print(rating)
        Feedback(comment = comment, rating = rating, user_id_host = user_host, user_id_comment = request.session['user_id_logged_in'], event_id=event_id).save()
        return redirect("../../profil")

    return render_page(request, 'feedback.html', {
        'check_existing_feedback': str(check_existing_feedback).lower()
    })


