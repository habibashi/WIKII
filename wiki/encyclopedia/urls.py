from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("createPage", views.createPage, name="createPage"),
    path("search", views.search, name="search"),
    path("wiki/<str:entry>/edit", views.edit, name="edit"),
    path("random", views.random, name="random")
]
