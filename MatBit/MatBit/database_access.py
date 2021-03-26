from datetime import datetime

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpRequest
from django.utils import timezone

from .mymodels import User, Registration, DinnerEvent


def is_logged_in(request: HttpRequest) -> bool:
    return 'user_id_logged_in' in request.session


def has_admin_privileges(request: HttpRequest) -> bool:
    token = request.session['admin_token']

    if token == 1:
        return True
    elif token == 0:
        return False
    else:
        raise ValueError(token)


def get_in_dinner(request: HttpRequest, event_id: int) -> Registration or None:
    try:
        return Registration.registrations.get(user_id=request.session['user_id_logged_in'], event_id=event_id)
    except ObjectDoesNotExist:  # Could've used Registration.DoesNotExist, but this saves us a warning suppression.
        return None


def create_dinner(
    name: str,
    description: str,
    capacity: int,
    location: str,
    date: str,
    time: str,
    cost: int,
) -> DinnerEvent:
    date_and_time = date + " " + time + ":00"

    dinner = DinnerEvent(
        name=name,
        description=description,
        capacity=capacity,
        location=location,
        date=date_and_time,
        creation_date=timezone.now(),
        cost=cost,
        is_cancelled=0
    )

    dinner.save()

    return dinner


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
    # TODO: should send e-mail with validation token

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
