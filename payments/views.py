from django.views.generic import TemplateView, View, FormView
from django.urls import reverse_lazy
from payments.models import BankDetails, Purchase, PurchaseProduct, GiftCode
from design.models import Designs
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse
from shoping_cart.cart import Cart
from payments.stripe_api import StripeAPI
from django.conf import settings
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_exempt
from honeypot.decorators import honeypot_exempt
from payments.forms import PurchaseForm
from django.contrib import messages
from django.utils.decorators import method_decorator
from decimal import Decimal
import uuid
import stripe

class CheckoutView(FormView):
    template_name = 'payments/payment.html'
    form_class = PurchaseForm
    success_url = reverse_lazy('purchase_confirmation')

    def form_valid(self, form):
        cart_items = self.request.session.get('cart', {})
        if not cart_items:
            form.add_error(None, 'Jūsu grozs ir tukšs.')
            return self.form_invalid(form)

        discount_value = self.check_gift_code(form, cart_items)
        amount = sum(Decimal(item.get('price', '0')) * Decimal(item.get('quantity', '1')) for item in cart_items.values())
        amount -= discount_value

        purchase = self.create_purchase(form, amount, discount_value)
        self.save_cart_items_to_purchase(cart_items, purchase)
        self.request.session['purchase_id'] = purchase.id

        if purchase.payment_method == 'BANK_TRANSFER':
            return redirect('payments:bank_details')
        elif purchase.payment_method == 'STRIPE':
            return redirect('payments:stripe_checkout')

        del self.request.session['cart']
        return redirect(self.success_url)

    def check_gift_code(self, form, cart_items):
        gift_code_str = form.cleaned_data.get('gift_code')
        discount_value = Decimal(0)

        if gift_code_str:
            try:
                gift_code = GiftCode.objects.get(code=gift_code_str)
                if not gift_code.is_active():
                    form.add_error('gift_code', 'Dāvanu kods nav derīgs vai ir beidzies tā derīguma termiņš.')
                    return self.form_invalid(form)
                else:
                    original_amount = sum(Decimal(item.get('price', '0')) * Decimal(item.get('quantity', '1')) for item in cart_items.values())
                    discount_value = self.apply_discount(gift_code, original_amount)
                    gift_code.use()
            except GiftCode.DoesNotExist:
                form.add_error(_('gift_code'), _('Šāds dāvanu kods nepastāv.'))
                return self.form_invalid(form)

        return discount_value

    def apply_discount(self, gift_code, original_amount):
        discount_value = Decimal(gift_code.discount_value)
        if gift_code.discount_type == 'percentage':
            return original_amount * (discount_value / 100)
        return discount_value

    def create_purchase(self, form, amount, discount_value):
        purchase = form.save(commit=False)
        purchase.user = self.request.user
        purchase.amount = amount
        purchase.discount_amount = discount_value
        purchase.save()
        return purchase

    def save_cart_items_to_purchase(self, cart_items, purchase):
        for product_id, product_data in cart_items.items():
            quantity = product_data.get('quantity', 1)
            if Designs.objects.filter(id=product_id).exists():
                PurchaseProduct.objects.create(
                    purchase=purchase,
                    product_id=product_id,
                    quantity=quantity
                )

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


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

        purchase_id = self.request.session.get('purchase_id')
        if purchase_id:
            try:
                purchase = Purchase.objects.get(id=purchase_id)
                context['order_number'] = purchase.order_number
                context['amount'] = purchase.amount
            except Purchase.DoesNotExist:
                return redirect('shopping_cart:cart')
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


class StripeCheckoutView(View):
    def get_existing_purchase(self, request):
        purchase_id = request.session.get('purchase_id')
        if not purchase_id:
            return None, 0, None
        try:
            purchase = Purchase.objects.get(id=purchase_id)
            amount = purchase.amount * 100
            order_number = purchase.order_number
            return purchase, amount, order_number
        except Purchase.DoesNotExist:
            return None, 0, None

    def get(self, request, *args, **kwargs):
        stripe_api = StripeAPI()
        purchase, amount, order_number = self.get_existing_purchase(request)

        if not purchase:
            return redirect('cart')

        cart_items = request.session.get('cart', {})
        line_items = []

        original_total = sum(float(item.get('price', 0)) * float(item.get('quantity', 1)) for item in cart_items.values())
        total_discount = float(purchase.discount_amount)
        discount_ratio = total_discount / original_total if original_total > 0 else 0

        for product_id, product_data in cart_items.items():
            price = float(product_data['price'])
            quantity = product_data['quantity']
            discounted_price = price * (1 - discount_ratio)
            unit_amount = int(discounted_price * 100)

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
                    'unit_amount': unit_amount,
                },
                'quantity': quantity,
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

        try:
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
        except Exception as e:
            return HttpResponse(f'Error creating checkout session: {str(e)}', status=500)


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
