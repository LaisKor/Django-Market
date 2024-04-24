from django.urls import path
from . import views

app_name = 'items'

urlpatterns = [
    path('create/', views.item_create, name='item_create'),
    path('<int:item_id>/', views.item_detail, name='item_detail'),
    path('<int:item_id>/update/', views.item_update, name='item_update'),
    path('<int:item_id>/delete/', views.item_delete, name='item_delete'),
    path('<int:item_id>/toggle_like/', views.toggle_like, name='toggle_like'),
]