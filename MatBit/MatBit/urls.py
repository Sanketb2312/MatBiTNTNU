from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
path('', views.frontpage, name='frontpage'),
path('registrering/', views.register, name='register'),
path('innlogging/', views.login, name='login'),
path('utlogging/', views.logout, name='logout'),
path('profil/', views.profile, name='profile'),
path('profil/rediger/', views.editUser, name='editUser')
]
