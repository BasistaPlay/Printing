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
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from payments.stripe_api import StripeAPI
from django.utils.translation import gettext as _
import stripe
from honeypot.decorators import honeypot_exempt

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
                if purchase.is_paid:
                    del self.request.session['purchase_id']
                    return self.create_new_purchase(context)
                else:
                    context['order_number'] = purchase.order_number
                    context['amount'] = purchase.amount
            except Purchase.DoesNotExist:
                del self.request.session['purchase_id']
                return self.create_new_purchase(context)
        else:
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
            created_at=timezone.now(),
            payment_method = 'BANK_TRANSFER'
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
        return redirect('payments:bank_transfer_success')



class PaymentConfirmationBaseView(TemplateView):
    template_name = 'payments/transfer_confirmation.html'
    success_message = ""
    follow_up_message = ""
    show_important_message = ""

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        cart.clear()

        context = self.get_context_data(**kwargs)
        context['success_message'] = self.success_message
        context['follow_up_message'] = self.follow_up_message
        context['show_important_message'] = self.show_important_message
        return self.render_to_response(context)


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

# stripe_integration/views.py

class StripeCheckoutView(View):
    def create_new_purchase(self, request):
        cart_items = request.session.get('cart', {})
        amount = sum(float(item.get('price', 0)) * float(item.get('quantity', 1)) for item in cart_items.values()) * 100

        if amount == 0:
            return None, 0, None
        order_number = f'ORD-{uuid.uuid4().hex[:6].upper()}'

        purchase = Purchase.objects.create(
            order_number=order_number,
            amount=amount / 100,
            user=request.user,
            is_paid=False,
            created_at=timezone.now(),
            payment_method = 'STRIPE'
        )

        for product_id, product_data in cart_items.items():
            quantity = product_data.get('quantity', 1)

            if Designs.objects.filter(id=product_id).exists():
                PurchaseProduct.objects.create(
                    purchase=purchase,
                    product_id=product_id,
                    quantity=quantity
                )

        request.session['purchase_id'] = purchase.id
        return purchase, amount, order_number

    def get(self, request, *args, **kwargs):
        stripe_api = StripeAPI()
        purchase, amount, order_number = self.create_new_purchase(request)

        if not purchase:
            return redirect('cart')

        cart_items = request.session.get('cart', {})
        line_items = []

        for product_id, product_data in cart_items.items():
            image_url = product_data.get('image')
            if image_url:
                image_url = request.build_absolute_uri(image_url)
            else:
                image_url = None

            line_items.append({
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': f'Product {product_id}',
                        'images': [image_url] if image_url else [],
                    },
                    'unit_amount': int(float(product_data['price']) * 100),
                },
                'quantity': product_data['quantity'],
            })

        shipping_cost = 5.00
        line_items.append({
            'price_data': {
                'currency': 'eur',
                'product_data': {
                    'name': 'Shipping',
                },
                'unit_amount': int(shipping_cost * 100),
            },
            'quantity': 1,
        })

        checkout_url = stripe_api.create_checkout_session(
            line_items=line_items,
            success_url=request.build_absolute_uri('/payments/payment-success/stripe/'),
            cancel_url=request.build_absolute_uri('/cart/'),
            client_reference_id=order_number
        )

        if checkout_url:
            return redirect(checkout_url)
        else:
            return HttpResponse('Error creating checkout session', status=500)

class StripeWebhookView(View):
    @method_decorator(csrf_exempt)
    @method_decorator(honeypot_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        stripe_api = StripeAPI()
        payload = request.body.decode('utf-8')
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')

        try:
            event = stripe_api.handle_webhook(payload, sig_header)
            event_type = event.get('type')

            if event_type == 'checkout.session.completed':
                session = event['data']['object']

                order_number = session.get('client_reference_id')
                purchase = Purchase.objects.filter(order_number=order_number).first()

            elif event_type == 'charge.succeeded':
                charge = event['data']['object']

            elif event_type == 'payment_intent.succeeded':
                payment_intent = event['data']['object']

            return HttpResponse(f"Event type {event_type} processed", status=200)

        except ValueError as e:
            return HttpResponse('Invalid payload', status=400)
        except stripe.error.SignatureVerificationError as e:
            return HttpResponse('Invalid signature', status=400)




class BankTransferConfirmationView(PaymentConfirmationBaseView):
    success_message = _("Paldies par jūsu pasūtījumu!")
    follow_up_message = _("Jūsu maksājuma procesa apstiprinājums ir saņemts. Kad mēs apstiprināsim jūsu apmaksu, mēs nosūtīsim apstiprinājuma e-pastu uz jūsu norādīto adresi.")
    show_important_message = _("Svarīgi! Jūs nevarēsiet veikt turpmākus pasūtījumus ar šo maksājuma metodi, kamēr mēs neapstiprināsim jūsu pašreizējo maksājumu.")

class StripePaymentConfirmationView(PaymentConfirmationBaseView):
    success_message = _("Paldies par jūsu Stripe maksājumu!")
    follow_up_message = _("Jūsu maksājums ar Stripe ir veiksmīgi apstiprināts. Mēs esam nosūtījuši apstiprinājuma e-pastu uz jūsu norādīto adresi.")