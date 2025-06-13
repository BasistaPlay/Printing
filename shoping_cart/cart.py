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

    def _build_key(self, design_id, size=None):
        """Palīgfunkcija, lai izveidotu unikālu atslēgu pēc ID un izmēra."""
        design_id = str(design_id)
        return f"{design_id}_{size}" if size else design_id

    def add(self, designs, quantity=1, sizes=None, product_id=0):
        """
        Pievieno produktu grozam. Ja ir vairāki izmēri, katrs ir atsevišķs ieraksts.
        """
        for size in sizes or [None]:  # Ja nav izmēru, būs tikai viens ieraksts
            key = self._build_key(designs.id, size)

            if key not in self.cart:
                self.cart[key] = {
                    'userid': self.request.user.id,
                    'product_id': designs.id,
                    'quantity': int(quantity),
                    'price': str(designs.product.price),
                    'total_price': str(designs.product.price * int(quantity)),
                    'image': designs.front_image.url if designs.front_image else '',
                    'sizes': [size] if size else [],
                    'design_id': product_id,
                }
            else:
                item = self.cart[key]
                item['quantity'] += int(quantity)
                item['total_price'] = str(Decimal(item['price']) * item['quantity'])

        self.save()

    def save(self):
        """Saglabā groza statusu sesijā."""
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, design_id, size=None):
        """
        Izņem konkrētu produktu pēc design ID un izmēra (ja ir).
        """
        key = self._build_key(design_id, size)
        if key in self.cart:
            del self.cart[key]
            self.save()

    def decrement(self, design_id, size=None):
        """
        Samazina daudzumu. Ja daudzums ir <1, produkts tiek izņemts.
        """
        key = self._build_key(design_id, size)
        if key in self.cart:
            self.cart[key]['quantity'] -= 1
            if self.cart[key]['quantity'] < 1:
                self.remove(design_id, size)
            else:
                self.cart[key]['total_price'] = str(
                    Decimal(self.cart[key]['price']) * self.cart[key]['quantity']
                )
                self.save()

    def clear(self):
        """Attīra visu grozu."""
        self.session[settings.CART_SESSION_ID] = {}
        self.session.modified = True


from decimal import Decimal

def cart_total_amount(request):
    cart = request.session.get(settings.CART_SESSION_ID, {})
    total_bill = Decimal('0.00')

    for key, value in cart.items():
        try:
            price = Decimal(value.get('price', '0.00'))
            quantity = int(value.get('quantity', 0))
            total_bill += price * quantity
        except (ValueError, TypeError):
            continue

    return {'total_bill': total_bill}