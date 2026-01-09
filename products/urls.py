from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.GuitarList.as_view(), name='guitar_list'),
    path('guitars/<int:pk>/', views.GuitarDetail.as_view(), name='guitar_detail'),
    path('accessories/', views.AccesoriesList.as_view(), name='accessory_list'),
    path('accessories/<int:pk>/', views.AccessoryDetail.as_view(), name='accessory_detail')
]
