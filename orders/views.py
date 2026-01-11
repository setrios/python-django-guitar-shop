from django.shortcuts import render
from .forms import CheckoutForm
from cart.cart import Cart

# Create your views here.

def checkout_view(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CheckoutForm()
    return render(request, 'checkout.html', {'form': form})
