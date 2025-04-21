from django.shortcuts import render, redirect
from .models import Item
from .forms import ItemForm


def home_view(request):
    return render(request, "home.html")


def items_list_view(request):
    items = Item.objects.all()
    print(items)
    return render(request, "items.html", {"items": items})


def create_item_view(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.save()
            return redirect('items_list')
    else:
        form = ItemForm()
    return render(request, "create_item.html", {"form": form})


def edit_item_view(request, id):
    item = Item.objects.get(id=id)
    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('items_list')
    else:
        form = ItemForm(instance=item)
    return render(request, "edit_item.html", {"form": form, "edit": True})


def delete_item_view(request, id):
    item = Item.objects.get(id=id)
    if request.method == "POST":
        item.delete()
        return redirect('items_list')
    return redirect('items_list')
