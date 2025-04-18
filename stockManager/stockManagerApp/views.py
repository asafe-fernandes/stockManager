from django.shortcuts import render, redirect
from .models import Item
from .forms import ItemForm


def home(request):
    return render(request, "home.html")


def items(request):
    items = Item.objects.all()
    return render(request, "items.html", {"items": items})


def createItem(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('itens')
    else:
        form = ItemForm()
    return render(request, "create_item.html", {"form": form})
