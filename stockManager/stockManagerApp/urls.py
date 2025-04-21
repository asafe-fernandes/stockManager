from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("items/", views.items_list_view, name="items_list"),
    path("items/add", views.create_item_view, name="create_item"),
    path("items/edit/<int:id>/", views.edit_item_view, name="edit_item"),
    path("items/delete/<int:id>/", views.delete_item_view, name="delete_item")
]
