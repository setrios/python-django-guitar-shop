from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from .cart import Cart
from products.models import Guitar, Accessory

# Create your views here.

class CartSummary(TemplateView):
    template_name = 'cart.html'


@require_POST
def add_product_ajax(request, product_pk):
    # Check if it's an AJAX request
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': False,
            'error': 'Invalid request'
        }, status=400)
    
    # get the product
    guitar = get_object_or_404(Guitar, pk=product_pk)

    # get and validate quantity
    try: 
        quantity = int(request.POST.get('quantity', 1))
    except (ValueError, TypeError):
        return JsonResponse({
            'success': False,
            'error': 'Invalid quantity'
        }, status=400)
    
    # validate quantity range
    if quantity < 1 or quantity > 99:
        return JsonResponse({
            'success': False,
            'error': 'Quantity must be between 1 and 99'
        }, status=400)
    
    # Add to cart
    cart = Cart(request)
    cart.add_product(product=guitar, quantity=quantity)

    return JsonResponse({
        'success': True,
        'message': f'Added {quantity} x {guitar.name} to cart',
        'cart_count': len(cart),
        'cart_total': str(cart.get_sub_total_price())
    })


@require_POST
def delete_product(request, product_pk):
    # Check if it's an AJAX request
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': False,
            'error': 'Invalid request'
        }, status=400)
    
    cart = Cart(request)
    guitar = get_object_or_404(Guitar, pk=product_pk)
    cart.remove_product(guitar)
    
    return JsonResponse({
        'success': True,
        'message': f'Removed {guitar.name} from cart',
        'cart_count': len(cart),
        'cart_total': str(cart.get_sub_total_price())
    })


@require_POST
def update_product_quantity(request, product_pk):
    # Check if it's an AJAX request
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': False,
            'error': 'Invalid request'
        }, status=400)
    
    cart = Cart(request)
    guitar = get_object_or_404(Guitar, pk=product_pk)
    action = request.POST.get('action')

    try:
        if action == 'increase':
            cart.change_product(guitar, 1)
        elif action == 'decrease':
            cart.change_product(guitar, -1) 
        else:
            return JsonResponse({
                'success': False,
                'error': 'Invalid action'
            }, status=400)
        
        return JsonResponse({
            'success': True,
            'message': f'Updated {guitar.name} quantity.',
            'cart_count': len(cart),
            'cart_total': str(cart.get_sub_total_price())
        })
    except ValueError as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

