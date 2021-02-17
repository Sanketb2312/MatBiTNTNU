from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.frontpage, name='forside'),
path('register/', views.register, name="register")
]