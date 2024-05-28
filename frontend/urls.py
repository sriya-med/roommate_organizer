from django.urls import path
from . import views
from .views import index

urlpatterns = [
    path('', index),
    path('Login', views.login, name='Login'),
    path('Registration', views.registration, name='Registration'),
    path('Homepage', views.homepage, name='Roomie'),
    path('Calendar', views.calendar, name='Calendar'),
    path('RoomieVal', views.RoomieVal, name='RoomieVal'),
    path('logout', views.logout, name='logout'),
]
