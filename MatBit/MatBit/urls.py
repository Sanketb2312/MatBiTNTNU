from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
path('', views.frontpage, name='frontpage'),
path('register/', views.register, name='register'),
path('logginn/', views.logginn, name='logginn'),
path('logout/', views.logout, name='logout')
]
