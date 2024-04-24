from django.shortcuts import render, redirect, get_object_or_404
from .models import Item
from .forms import ItemForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required 
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render(request, 'item_detail.html', {'item': item})

@login_required
def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)  
            item.author = request.user  
            item.save() 
            return redirect('items:item_detail', item_id=item.pk)  
    else:
        form = ItemForm()
    return render(request, 'item_create.html', {'form': form})

def item_delete(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.method == 'POST':
        item.delete()
        return redirect(reverse('mainpage:index')) 
    return render(request, 'items/confirm_delete.html', {'item': item})

@login_required
@csrf_exempt
def toggle_like(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(Item, id=item_id)
        liked = False
        if request.user in item.likes.all():
            item.likes.remove(request.user)
        else:
            item.likes.add(request.user)
            liked = True
        return JsonResponse({'liked': liked})
    
@login_required
def item_update(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if request.user != item.author:
        return redirect('items:item_detail', item_id=item.id)

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('items:item_detail', item_id=item.id)
    else:
        form = ItemForm(instance=item)
    
    return render(request, 'item_form.html', {'form': form, 'item': item})