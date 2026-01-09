from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartSummary.as_view(), name='cart_summary'),
    path('add/<int:product_pk>/', views.add_product_ajax, name='add_product'),
    path('delete/<int:product_pk>/', views.delete_product, name='delete_product'),
    path('update/<int:product_pk>/', views.update_product_quantity, name='update_product'),
]
