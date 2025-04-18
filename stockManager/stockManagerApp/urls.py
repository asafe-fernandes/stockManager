from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("items/", views.items, name="itens"),
    path("items/add", views.createItem, name="createItem"),
    path("items/edit/<int:id>/", views.editItem, name="editItem"),
]
