from .cart import Cart

# Context processors allow you to add variables to the context of every template automatically.
# This one adds the number of items in the cart and the cart subtotal so that they can be shown
# globally (e.g., in the navbar or header on every page).

def cart_processor(request):
    return {'cart': Cart(request)}