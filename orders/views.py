from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.urls import reverse
from django.conf import settings
from .models import Order, OrderItem
from .forms import CheckoutForm, CheckoutWithNewAddressForm
from cart.cart import Cart
from products.models import Guitar, Accessory

import stripe

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY

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

                    # here payments should be done
                    if order.payment_provider == 'stripe':
                        line_items = []
                        for item in cart_items:
                            line_items.append({
                                'price_data': {
                                    'currency': 'usd',
                                    'product_data': {
                                        'name': item['item'].name,
                                    },
                                    'unit_amount': int(item['item'].price * 100),
                                },
                                'quantity': item['quantity'],
                            })
                        
                        try:
                            checkout_session = stripe.checkout.Session.create(
                                payment_method_types=['card'],
                                line_items=line_items,
                                mode='payment',
                                success_url=request.build_absolute_uri(reverse('orders:success')) + '?session_id={CHECKOUT_SESSION_ID}',
                                cancel_url=request.build_absolute_uri(reverse('orders:cancel')) + f'?order_id={order.id}',
                                metadata={
                                    'order_id': str(order.id),
                                }
                            )
                            
                            # save session ID
                            order.stripe_payment_intent_id = checkout_session.id
                            order.save()
                            
                            return redirect(checkout_session.url)
                            
                        except stripe.error.StripeError as e:
                            messages.error(request, f'Stripe error: {str(e)}')
                            order.delete()
                            raise
                        except Exception as e:
                            messages.error(request, f'Payment setup error: {str(e)}')
                            order.delete()
                            raise

                    # clear the cart
                    cart.clear()
                    messages.success(request, f'Order #{order.id} created successfully!')
                    return redirect('accounts:home')
                
            except stripe.error.StripeError as e:
                messages.error(request, f'Stripe error: {str(e)}')    
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

def success(request):
    session_id = request.GET.get('session_id')
    
    if session_id:
        try:
            # verify the session
            session = stripe.checkout.Session.retrieve(session_id)
            
            # get the order
            order_id = session['metadata']['order_id']
            order = Order.objects.get(id=order_id, user=request.user)
            
            cart = Cart(request)

            # update produts quantities
            for product_item in cart.products():
                product = Guitar.objects.get(pk=product_item['item'].pk)
                product.stock -= product_item['quantity']
                if product.stock <= 0:
                    product.is_avaliable = False
                product.save()

            for accessory_item in cart.accessories():
                accessory = Accessory.objects.get(pk=accessory_item['item'].pk)
                accessory.stock -= product_item['quantity']
                if accessory.stock <= 0:
                    accessory.is_avaliable = False
                accessory.save()

            # clear the cart after successful payment
            cart.clear()
            
            messages.success(request, f'Order #{order.id} paid successfully!')
            
            context = {
                'order': order,
            }
            return render(request, 'success.html', context)
            
        except stripe.error.StripeError as e:
            messages.error(request, 'Could not verify payment session')
        except Order.DoesNotExist:
            messages.error(request, 'Order not found')
    
    return render(request, 'success.html')

def cancel(request):
    order_id = request.GET.get('order_id')
    
    if order_id:
        try:
            # delete the cancelled order
            order = Order.objects.get(id=order_id, user=request.user)
            order.delete()
            messages.info(request, 'Payment cancelled. Order has been removed.')
        except Order.DoesNotExist:
            pass
    
    return render(request, 'cancel.html')


from django.views.generic import DetailView

class OrderDetail(DetailView):
    model = Order
    template_name = 'order_detail.html'
