from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
path('', views.frontpage, name='frontpage'),
path('registrering/', views.register, name='register'),
path('innlogging/', views.login, name='login'),
path('utlogging/', views.logout, name='logout'),
path('profil/', views.profile, name='profile'),
path('nyMiddag/', views.newMeal, name = 'newMeal'),
path('oversikt/', views.mealOverview, name = 'mealOverview'),
path('profil/', views.profile, name='profile'),
path('profil/rediger/', views.editUser, name='editUser'),
path('oversikt/middag/<int:arrangementid>', views.chooseMeal, name='chooseMeal'),
path('profil/addallergies/', views.addAllergies, name='addAllergies')
]
