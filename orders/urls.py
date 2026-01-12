from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.checkout_view, name='checkout'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
]
