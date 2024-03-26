from django.urls import path
from .views import item_list, item_detail, item_new, item_edit, item_delete, register, user_login

urlpatterns = [
    path('item/', item_list, name='item_list'),
    path('item/new/', item_new, name='item_new'),
    path('item/detail/<int:pk>/', item_detail, name='item_detail'),
    path('item/edit/<int:pk>/', item_edit, name='item_edit'),
    path('item/delete/<int:pk>/', item_delete, name='item_delete'),
    path('', item_list, name='crud_home'),
    path('crud/item/detail/<int:pk>/', item_detail, name='item_detail'),  # Remove 'views.'
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),  # Use 'user_login' instead of 'login'
    # other patterns
]
