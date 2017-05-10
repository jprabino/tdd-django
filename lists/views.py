from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.
from lists.forms import ItemForm
from lists.models import Item, List
import inspect

def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None
    if request.method == 'POST':
        try:
            item=Item(text=request.POST['name'], list=list_)

            item.full_clean()
            item.save()
            return redirect(list_)
        except ValidationError:
            error = "No se puede ingresar un item vacío"

    return render(request, 'list.html', {'list': list_, 'error': error})

def new_list(request):
    list_= List.objects.create()
    item = Item.objects.create(text=request.POST['name'], list=list_)
    try:
        item.full_clean()
    except ValidationError:
        list_.delete()
        error = "No se puede ingresar un item vacío"
        return render(request, 'home.html', {'error': error})

    return redirect(list_)
