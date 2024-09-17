from django.views.generic import TemplateView
from django.urls import reverse_lazy
from payments.models import BankDetails, Purchase, PurchaseProduct
from design.models import Designs
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import View
from django.conf import settings
import uuid
from shoping_cart.cart import Cart

from django.shortcuts import redirect

class BankDetailsView(TemplateView):
    template_name = 'payments/bank_details.html'

    def dispatch(self, request, *args, **kwargs):
        cart_items = request.session.get('cart', {})

        if not cart_items:
            return redirect('shopping_cart:cart')

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bank_details'] = BankDetails.objects.first()
        context['order_number'] = None

        purchase_id = self.request.session.get('purchase_id')

        if purchase_id:
            try:
                purchase = Purchase.objects.get(id=purchase_id)
                # Ja pasūtījums ir apmaksāts, izdzēš sesijas purchase_id
                if purchase.is_paid:
                    del self.request.session['purchase_id']
                    # Izveido jaunu pasūtījumu
                    return self.create_new_purchase(context)
                else:
                    context['order_number'] = purchase.order_number
                    context['amount'] = purchase.amount
            except Purchase.DoesNotExist:
                del self.request.session['purchase_id']
                # Ja pasūtījuma nav, izveido jaunu pasūtījumu
                return self.create_new_purchase(context)
        else:
            # Ja nav purchase_id, izveido jaunu pasūtījumu
            return self.create_new_purchase(context)

        return context

    def create_new_purchase(self, context):
        cart_items = self.request.session.get('cart', {})
        amount = sum(float(item.get('price', 0)) * float(item.get('quantity', 1)) for item in cart_items.values())
        order_number = f'ORD-{uuid.uuid4().hex[:6].upper()}'

        purchase = Purchase.objects.create(
            order_number=order_number,
            amount=amount,
            user=self.request.user,
            is_paid=False,
            created_at=timezone.now()
        )

        for product_id, product_data in cart_items.items():
            quantity = product_data.get('quantity', 1)

            if Designs.objects.filter(id=product_id).exists():
                PurchaseProduct.objects.create(
                    purchase=purchase,
                    product_id=product_id,
                    quantity=quantity
                )

        self.request.session['purchase_id'] = purchase.id
        context['order_number'] = order_number
        context['amount'] = amount

        return context

    def post(self, request, *args, **kwargs):
        return redirect('payments:payment_confirmation')



class PaymentConfirmationView(TemplateView):
    template_name = 'payments/transfer_confirmation.html'

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        cart.clear()
        return super().get(request, *args, **kwargs)


class CancelPurchaseView(View):
    def post(self, request, *args, **kwargs):
        purchase_id = request.session.get('purchase_id')

        if purchase_id:
            try:
                purchase = Purchase.objects.get(id=purchase_id)
                purchase.delete()
            except Purchase.DoesNotExist:
                pass

            del request.session['purchase_id']

        return redirect('shopping_cart:cart')