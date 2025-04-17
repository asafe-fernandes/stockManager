from django.shortcuts import render
from .models import Item
# Create your views here.


def home(request):
    return render(request, "home.html")


def items(request):
    items = Item.objects.all()
    return render(request, "items.html", {"items": items})
