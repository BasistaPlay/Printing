import stripe
from django.conf import settings
from payments.models import Purchase
from django.http import HttpResponse

class StripeAPI:
    def __init__(self):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        self.webhook_secret = settings.STRIPE_WEBHOOK_SECRET

    def create_checkout_session(self, line_items, success_url, cancel_url, client_reference_id):
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
                client_reference_id=client_reference_id
            )
            return session.url
        except Exception as e:
            return None

    def handle_webhook(self, payload, sig_header):
        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, self.webhook_secret
            )

            event_type = event.get('type')

            if event_type == 'checkout.session.completed':
                session = event['data']['object']

                order_number = session.get('client_reference_id')
                purchase = Purchase.objects.filter(order_number=order_number).first()

                if purchase:
                    purchase.is_paid = True
                    purchase.save()
                    return HttpResponse('Payment succeeded', status=200)
                else:
                    return HttpResponse('No purchase found', status=404)

            elif event_type == 'charge.updated':
                charge = event['data']['object']
                return HttpResponse('Charge updated processed', status=200)

            elif event_type == 'invoice.finalized':
                invoice = event['data']['object']
                return HttpResponse('Invoice finalized processed', status=200)

            return HttpResponse(f"Unhandled event type: {event_type}", status=200)

        except ValueError as e:
            return HttpResponse('Invalid payload', status=400)
        except stripe.error.SignatureVerificationError as e:
            return HttpResponse('Invalid signature', status=400)