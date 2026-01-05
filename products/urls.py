from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.GuitarList.as_view(), name='guitar_list'),
    path('guitars/<int:pk>/', views.GuitarDetail.as_view(), name='guitar_detail')
]
