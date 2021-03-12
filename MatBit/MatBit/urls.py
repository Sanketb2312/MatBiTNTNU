from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.frontpage, name='frontpage'),
    path('registrering/', views.register, name='register'),
    path('innlogging/', views.login, name='login'),
    path('utlogging/', views.logout, name='logout'),
    path('profil/', views.profile, name='profile'),
    path('nyMiddag/', views.new_meal, name='newMeal'),
    path('oversikt/', views.meal_overview, name='mealOverview'),
    path('profil/', views.profile, name='profile'),
    path('profil/rediger/', views.edit_user, name='editUser'),
    path('oversikt/middag/<int:arrangementid>', views.choose_meal, name='chooseMeal')
]
