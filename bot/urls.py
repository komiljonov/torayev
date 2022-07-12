from django.urls import path
from .views import register, home, videos




urlpatterns = [
    path('register', register),
    path('videos', videos),
    path('', home)
]