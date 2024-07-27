from decimal import Decimal
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect


class Cart(object):

    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

class Cart(object):
    def __init__(self, request):
        self.request = request
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, order, quantity=1, sizeCount=1, sizes=None, product_id=0):
        """
        Add a product to the cart or update its quantity.
        """
        id = order.id
        newItem = True
        
        if str(order.id) not in self.cart.keys():
            self.cart[order.id] = {
                'userid': self.request.user.id,
                'product_id': id,
                'quantity': int(quantity),
                'sizeCount': sizeCount,  # Use the sizeCount parameter here
                'price': str(order.product.price),
                'image': order.front_image.url if order.front_image else '',
                'sizes': sizes ,
                'order_id' : product_id ,
            }
        else:
            for key, value in self.cart.items():
                if key == str(order.id):
                    value['quantity'] += int(quantity)  # Add the quantity to existing quantity
                    value['sizeCount'] += sizeCount
                    if sizes:
                        for size in sizes:
                            if size['size'] in value['sizes']:
                                value['sizes'][size['size']] += size['count']
                            else:
                                value['sizes'][size['size']] = size['count']
                    newItem = False
                    self.save()
                    break
            
            if newItem:
                self.cart[order.id] = {
                    'userid': self.request.user.id,
                    'product_id': id,
                    'quantity': int(quantity),
                    'sizeCount': sizeCount,  # Use the sizeCount parameter here
                    'price': str(order.product.price),
                    'image': order.front_image.url if order.front_image else '',
                    'sizes': sizes, 
                    'order_id' : product_id ,
                }

        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True


    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, order):
        order_id = str(order.id)
        print(f"rfef{order_id}")
        if order_id in self.cart:
            del self.cart[order_id]
            self.save()

    def decrement(self, product):
        for key, value in self.cart.items():
            if key == str(product.id):

                value['quantity'] = value['quantity'] - 1
                if(value['quantity'] < 1):
                    return redirect('cart')
                self.save()
                break
            else:
                print("Something Wrong")

    def clear(self):
        # empty cart
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True


from decimal import Decimal

def cart_total_amount(request):
    cart = request.session.get(settings.CART_SESSION_ID, {})
    total_bill = Decimal('0.00')  # Initialize total_bill as Decimal for precise calculations

    for key, value in cart.items():
        try:
            price = Decimal(value.get('price', '0.00'))
            quantity = int(value.get('quantity', 0))
            total_bill += price * quantity
        except (ValueError, TypeError):
            continue  # Handle invalid data gracefully, e.g., log or ignore

    return {'total_bill': total_bill}