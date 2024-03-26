from django.shortcuts import render, get_object_or_404, redirect
from .models import Item
from .forms import ItemForm
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import login as auth_login 
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

def item_list(request):
    items = Item.objects.all()
    return render(request, 'item_list.html', {'items': items})

def item_detail(request, pk):
    items = Item.objects.all()
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'item_detail.html', {'items': items, 'item': item})

def item_new(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save()
            messages.success(request, 'Book created successfully!')
            return redirect('item_detail', pk=item.pk)
    else:
        form = ItemForm()
    
    return render(request, 'item_new.html', {'form': form})


def item_edit(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            messages.success(request, 'Book edited successfully!')
            return redirect('item_detail', pk=item.pk)
    else:
        form = ItemForm(instance=item)
    return render(request, 'item_edit.html', {'form': form})

def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.delete()
    return redirect('item_list')


# def register(request):
#     print("Register view is called.")
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             auth_login(request, user)
#             print("User registered:", user.username)
#             return redirect('item_list')
#         else:
#             print("Form errors:", form.errors)
#     else:
#         form = RegistrationForm()

#     return render(request, 'register.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, 'Successfully Registered!')
            
            # Log the user registration
            logger.info(f"User registered: {user.username}, email: {user.email}")

            return redirect('register')  # Redirect to the same page
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

def user_login(request):  # Renamed to avoid conflicts
    print("Login view is called.")
    print("Form data:", request.POST)
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)  # Use auth_login instead of login
            messages.success(request, 'Loged In successfully!')
            return redirect('item_list')  # Redirect to the item list page, for example
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})
