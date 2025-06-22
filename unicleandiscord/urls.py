"""Routes."""

from django.urls import path

from . import views

app_name = "unicleandiscord"

urlpatterns = [
    path("", views.index, name="index"),
]
