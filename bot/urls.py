from django.urls import path
from .views import register, home




urlpatterns = [
    path('register', register),
    path('', home)
]