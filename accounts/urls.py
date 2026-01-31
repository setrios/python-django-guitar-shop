from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('home/', views.HomePageView.as_view(), name='home'),
    path('address/new/', views.AddressCreateView.as_view(), name='address_new'),
    path('address/<int:pk>/edit/', views.AddressUpdateView.as_view(), name='address_edit'),
    path('address/<int:pk>/delete/', views.AddressDeleteView.as_view(), name='address_delete'),
]
