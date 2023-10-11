from django.urls import include, path
from . import views

urlpatterns = [
    path('hello/', views.say_hello),
]

