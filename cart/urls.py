from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartSummary.as_view(), name='cart_summary'),
    path('product/add/<int:product_pk>/', views.add_product_ajax, name='add_product'),
    path('product/delete/<int:product_pk>/', views.delete_product, name='delete_product'),
    path('product/update/<int:product_pk>/', views.update_product_quantity, name='update_product'),
    path('accessory/add/<int:accessory_pk>/', views.add_accessory_ajax, name='add_accessory'),
    path('accessory/delete/<int:accessory_pk>/', views.delete_accessory, name='delete_accessory'),
    path('accessory/update/<int:accessory_pk>/', views.update_accessory_quantity, name='update_accessory'),

]
