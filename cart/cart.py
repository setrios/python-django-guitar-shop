from products.models import Guitar, Accessory
from decimal import Decimal, ROUND_HALF_UP



class Cart():
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get('session_key')

        if not cart:
            cart = {'products': {}, 'accessories': {}}
            self.session['session_key'] = cart

        self.cart = cart


    def __count_item_total(self, item_price: Decimal, item_quantity: int) -> str:
        # return str(
        #     (item_price * item_quantity).quantize(
        #         Decimal('0.00'),
        #         rounding=ROUND_HALF_UP
        #     )
        # )

        # Since Python 3.3 you can use round() with a Decimal and it will return you a Decimal
        return str(round(item_price * item_quantity, 2))


    def add_product(self, product: Guitar, quantity=1):
        product_pk = str(product.pk)

        # check stock 
        product_quantity_in_cart = self.cart['products'].get(product_pk, {}).get('quantity', 0)
        if product_quantity_in_cart + quantity > product.stock:
            raise ValueError(f'Not enough stock for {product.name}')

        # add to cart
        if product_pk not in self.cart['products']:
            self.cart['products'][product_pk] = {'quantity': quantity, 'item_total': self.__count_item_total(product.price, quantity)}
        else:
            new_quantity = self.cart['products'][product_pk]['quantity'] + quantity
            self.cart['products'][product_pk]['quantity'] = new_quantity
            self.cart['products'][product_pk]['item_total'] = self.__count_item_total(product.price, new_quantity)

        self.session.modified = True


    def add_accessory(self, accessory: Accessory, quantity=1):
        accessory_pk = str(accessory.pk)

        # check stock 
        accessories_quantity_in_cart = self.cart['accessories'].get(accessory_pk, {}).get('quantity', 0)
        if accessories_quantity_in_cart + quantity > accessory.stock:
            raise ValueError(f'Not enough stock for {accessory.name}')

        # add to cart
        if accessory_pk not in self.cart['accessories']:
            self.cart['accessories'][accessory_pk] = {'quantity': quantity, 'item_total': self.__count_item_total(accessory.price, quantity)}
        else:
            new_quantity = self.cart['accessories'][accessory_pk]['quantity'] + quantity
            self.cart['accessories'][accessory_pk]['quantity'] = new_quantity
            self.cart['accessories'][accessory_pk]['item_total'] = self.__count_item_total(accessory.price, new_quantity)

        self.session.modified = True


    def remove_product(self, product: Guitar):
        product_pk = str(product.pk)
        
        if product_pk in self.cart['products']:
            del self.cart['products'][product_pk]
            self.session.modified = True


    def remove_accessory(self, accessory: Accessory):
        accessory_pk = str(accessory.pk)
        
        if accessory_pk in self.cart['accessories']:
            del self.cart['accessories'][accessory_pk]
            self.session.modified = True


    def update_product(self, product: Guitar, quantity):
        '''quantity: int - new absolute qunatity been set, not relative'''
        product_pk = str(product.pk)

        if quantity > product.stock:
            raise ValueError(f'Not enough stock for {product.name}')
        
        if quantity <= 0:
            self.remove_product(product)
        elif product_pk in self.cart['products']:
            self.cart['products'][product_pk]['quantity'] = quantity
            self.cart['products'][product_pk]['item_total'] = self.__count_item_total(product.price, quantity)
        else:
            raise ValueError(f'{product.name} is not in cart')

        self.session.modified = True

    def change_product(self, product: Guitar, to_add):
        '''Method to increment or decrement product quantity'''
        product_pk = str(product.pk)

        if product_pk not in self.cart['products']:
            raise ValueError(f'{product.name} is not in cart')
        
        new_quantity = self.cart['products'][product_pk]['quantity'] + to_add

        if new_quantity > product.stock:
            raise ValueError(f'Not enough stock for {product.name}')
        
        if new_quantity <= 0:
            self.remove_product(product)
        else:
            self.cart['products'][product_pk]['quantity'] = new_quantity
            self.cart['products'][product_pk]['item_total'] = self.__count_item_total(product.price, new_quantity)

        self.session.modified = True


    def update_accessory(self, accessory: Accessory, quantity):
        '''quantity: int - new absolute qunatity been set, not relative'''
        accessory_pk = str(accessory.pk)

        if quantity > accessory.stock:
            raise ValueError(f'Not enough stock for {accessory.name}')
        
        if quantity <= 0:
            self.remove_accessory(accessory)
        elif accessory_pk in self.cart['accessories']:
            self.cart['accessories'][accessory_pk]['quantity'] = quantity
            self.cart['accessories'][accessory_pk]['item_total'] = self.__count_item_total(accessory.price, quantity)
        else:
            raise ValueError(f'{accessory.name} is not in cart')
        
        self.session.modified = True


    def change_accessory(self, accessory: Accessory, to_add):
        '''Method to increment or decrement accessory quantity'''
        accessory_pk = str(accessory.pk)

        if accessory_pk not in self.cart['accessories']:
            raise ValueError(f'{accessory.name} is not in cart')
        
        new_quantity = self.cart['accessories'][accessory_pk]['quantity'] + to_add

        if new_quantity > accessory.stock:
            raise ValueError(f'Not enough stock for {accessory.name}')
        
        if new_quantity <= 0:
            self.remove_product(accessory)
        else:
            self.cart['accessories'][accessory_pk]['quantity'] = new_quantity
            self.cart['accessories'][accessory_pk]['item_total'] = self.__count_item_total(accessory.price, new_quantity)

        self.session.modified = True


    def clear(self):
        self.session['session_key'] = {}
        self.cart = self.session['session_key']
        self.session.modified = True


    # right implementation - only 2 requests to db
    def get_cart_items(self):
        product_pks = self.cart['products'].keys()
        accessory_pks = self.cart['accessories'].keys()

        products = {str(p.pk): p for p in Guitar.objects.filter(pk__in=product_pks)}    
        accessories = {str(a.pk): a for a in Accessory.objects.filter(pk__in=accessory_pks)}

        cart_items = []
        for product_pk, data in self.cart['products'].items():
            if product_pk in products:
                cart_items.append({
                    'item': products[product_pk],
                    'quantity': data['quantity'],
                    'item_total': Decimal(data['item_total'])
                })

        for accessory_pk, data in self.cart['accessories'].items():
            if accessory_pk in accessories:
                cart_items.append({
                    'item': accessories[accessory_pk],
                    'quantity': data['quantity'],
                    'item_total': Decimal(data['item_total'])
                })

        return cart_items


    # # bad implementation - n + 1 query problem - too many requests to db
    # def get_cart_items(self):
    #     cart_items = []
    #     for product_pk, product_entry_data in self.cart['products'].items():
    #         item = Guitar.objects.get(pk=product_pk)
    #         quantity = product_entry_data['quantity']
    #         item_total = Decimal(product_entry_data['item_total'])
    #
    #         cart_items.append({
    #             'item': item,
    #             'quantity': quantity,
    #             'item_total': item_total
    #         })
    #
    #     for accessory_pk, accessory_entry_data in self.cart['accessories'].items():
    #         item = Accessory.objects.get(pk=accessory_pk)
    #         quantity = accessory_entry_data['quantity']
    #         item_total = Decimal(accessory_entry_data['item_total'])
    #
    #         cart_items.append({
    #             'item': item,
    #             'quantity': quantity,
    #             'item_total': item_total
    #         })
    #
    #     return cart_items


    def get_sub_total_price(self):
        if self.cart:
            products_subtotal = sum(Decimal(product_entry_data['item_total']) for product_entry_data in self.cart['products'].values())
            accessories_subtotal = sum(Decimal(accessory_entry_data['item_total']) for accessory_entry_data in self.cart['accessories'].values())
            return products_subtotal + accessories_subtotal
        else:
            return 0
    

    def __len__(self):
        if self.cart:
            products_count = sum(product_entry_data['quantity'] for product_entry_data in self.cart['products'].values())
            accessories_count = sum(accessory_entry_data['quantity'] for accessory_entry_data in self.cart['accessories'].values())
            return products_count + accessories_count
        else:
            return 0
        
    def __iter__(self):
        product_pks = self.cart['products'].keys()
        accessory_pks = self.cart['accessories'].keys()

        products = {str(p.pk): p for p in Guitar.objects.filter(pk__in=product_pks)}
        accessories = {str(a.pk): a for a in Accessory.objects.filter(pk__in=accessory_pks)}

        for product_pk, data in self.cart['products'].items():
            if product_pk in products:
                yield {
                    'item': products[product_pk],
                    'quantity': data['quantity'],
                    'item_total': Decimal(data['item_total'])
                }

        for accessory_pk, data in self.cart['accessories'].items():
            if accessory_pk in accessories:
                yield {
                    'item': accessories[accessory_pk],
                    'quantity': data['quantity'],
                    'item_total': Decimal(data['item_total'])
                }