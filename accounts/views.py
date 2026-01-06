from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import ShippingAddress

# Create your views here.

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class HomePageView(LoginRequiredMixin, UpdateView):
    template_name = 'home.html'
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('accounts:home')

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['addresses'] = ShippingAddress.objects.filter(user=self.request.user)
        return context
    

class AddressCreateView(LoginRequiredMixin, CreateView):
    model = ShippingAddress
    template_name = 'address_new.html'
    success_url = reverse_lazy('accounts:home')
    fields = (
        'address1',
        'address2',
        'city',
        'state',
        'country',
        'postal_code',
    )

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    

class AddressUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ShippingAddress
    template_name = 'address_edit.html'
    success_url = reverse_lazy('accounts:home')
    fields = (
        'address1',
        'address2',
        'city',
        'state',
        'country',
        'postal_code',
    )

    def test_func(self):
        obj = self.get_object()  # returns the ShippingAddress instance being edited
        return obj.user == self.request.user
    

class AddressDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ShippingAddress
    template_name = 'address_delete.html'
    success_url = reverse_lazy('accounts:home')

    def test_func(self):
        obj = self.get_object()  # returns the ShippingAddress instance being edited
        return obj.user == self.request.user