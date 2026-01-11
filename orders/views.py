from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from .models import Order, OrderItem
from .forms import CheckoutForm, CheckoutWithNewAddressForm
from cart.cart import Cart

# Create your views here.

@login_required
def checkout_view(request):
    cart = Cart(request)
    total = cart.get_sub_total_price()
    
    if not cart.get_cart_items():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:cart_summary') 
    
    # if user wants to add a new address
    add_new_address = (request.GET.get('add_new') == 'true') or (request.POST.get('add_new_address') == 'true')
    
    # if user has existing addresses
    has_addresses = request.user.addresses.exists()
    
    if has_addresses and not add_new_address:
        FormClass = CheckoutForm
        show_new_address_form = False
    else:
        FormClass = CheckoutWithNewAddressForm
        show_new_address_form = True
    
    if request.method == 'POST':
        if FormClass == CheckoutForm:
            form = FormClass(request.POST, user=request.user)
        else:
            form = FormClass(request.POST)
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    order = form.save(commit=False)
                    order.user = request.user
                    order.total_price = total
                    
                    # handle address creation if using new address form
                    if isinstance(form, CheckoutWithNewAddressForm):
                        address = form.save_address(request.user)
                        order.address = address
                    
                    order.save()
                    
                    # create order items
                    cart_items = cart.get_cart_items()
                    for item in cart_items:
                        OrderItem.objects.create(
                            order=order,
                            product=item['item'],
                            quantity=item['quantity'],
                            price=item['item_total']
                        )
                    
                    # clear the cart
                    cart.clear()
                    
                    messages.success(request, f'Order #{order.id} created successfully!')
                    return redirect('accounts:home')
                    
            except Exception as e:
                messages.error(request, f'An error occurred while processing your order: {str(e)}')
    else:
        if FormClass == CheckoutForm:
            form = FormClass(user=request.user)
        else:
            form = FormClass()
    
    context = {
        'form': form,
        'total': total,
        'has_addresses': has_addresses,
        'show_new_address_form': show_new_address_form,
        'cart': cart,
    }
    
    return render(request, 'checkout.html', context)