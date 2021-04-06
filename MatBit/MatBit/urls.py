from django.urls import path
from django.conf.urls import url
from . import views

# noinspection SpellCheckingInspection
urlpatterns = [
    path('', views.frontpage, name='frontpage'),
    path('registrering/', views.register, name='register'),
    path('innlogging/', views.login, name='login'),
    path('utlogging/', views.logout, name='logout'),
    path('profil/', views.profile, name='profile'),
    path('nyMiddag/', views.new_meal, name='newMeal'),
    path('oversikt/', views.meal_overview, name='mealOverview'),
    path('profil/', views.profile, name='profile'),
    path('profil/allergier/', views.add_allergies, name='addAllergies'),
    path('profil/rediger/', views.edit_user, name='editUser'),
    path('brukere/', views.profiles_list, name='profilesList'),
    path('oversikt/middag/<int:event_id>', views.choose_meal, name='chooseMeal'),
    path('oversikt/middag/<int:event_id>/rediger/', views.edit_meal, name='editMeal'),
]
