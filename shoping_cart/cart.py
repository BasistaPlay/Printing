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

    def add(self, designs, quantity=1, sizeCount=1, sizes=None, product_id=0):
        """
        Add a product to the cart or update its quantity.
        """
        id = designs.id
        newItem = True

        if str(designs.id) not in self.cart.keys():
            self.cart[designs.id] = {
                'userid': self.request.user.id,
                'product_id': id,
                'quantity': int(quantity),
                'sizeCount': sizeCount,
                'price': str(designs.product.price),
                'total_price': str(designs.product.price * int(quantity)),
                'image': designs.front_image.url if designs.front_image else '',
                'sizes': sizes ,
                'design_id' : product_id ,
            }
        else:
            for key, value in self.cart.items():
                        if key == str(designs.id):
                            value['quantity'] += int(quantity)
                            value['sizeCount'] += sizeCount
                            value['total_price'] = str(designs.product.price  * value['quantity'])  # Atjaunina kopējo cenu
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
                self.cart[designs.id] = {
                    'userid': self.request.user.id,
                    'product_id': id,
                    'quantity': int(quantity),
                    'sizeCount': sizeCount,  # Use the sizeCount parameter here
                    'price': str(designs.product.price),
                    'total_price': str(designs.product.price * int(quantity)),
                    'image': designs.front_image.url if designs.front_image else '',
                    'sizes': sizes,
                    'design_id' : product_id ,
                }

        self.save()

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True


    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, designs):
        design_id = str(designs.id)
        if design_id in self.cart:
            del self.cart[design_id]
            self.save()

    def decrement(self, designs):
        for key, value in self.cart.items():
            if key == str(designs.id):
                value['quantity'] = value['quantity'] - 1
                value['total_price'] = str(Decimal(value['price']) * value['quantity'])
                if value['quantity'] < 1:
                    self.remove(designs)
                self.save()
                break

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