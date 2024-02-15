from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path("newpage/", views.newpage, name="newpage"),
    path("editpage", views.editpage, name="editpage"),
    path("randompage/", views.randompage, name="randompage"),
    path("save_edit/", views.save_edit, name="save_edit")
]