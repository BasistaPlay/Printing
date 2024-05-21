import logging
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from stripe_integration.models import StripeKeys
from home.models import CustomDesign, Purchase, Order, PurchaseProduct
import stripe
from django.views.generic import TemplateView

stripe_keys = StripeKeys.objects.first()
if stripe_keys:
    stripe_public_key = stripe_keys.public_key
    stripe_secret_key = stripe_keys.secret_key
    stripe_endpoint_secret = stripe_keys.endpoint_secret
    stripe.api_key = stripe_secret_key
else:
    logger.error("Stripe keys are not set up in the database.")
    stripe_public_key = stripe_secret_key = stripe_endpoint_secret = None

@csrf_exempt
@login_required(login_url='/account/login/')
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': stripe_public_key}
        return JsonResponse(stripe_config, safe=False)

def create_checkout_session(request):
    user = request.user
    stripe.api_key = stripe_secret_key
    products_in_cart = request.session.get('cart', {})
    
    if not products_in_cart:
        return JsonResponse({'error': 'The cart is empty'})
    
    product_id_list = []
    product_id_list = ",".join(str(product_info['product_id']) for product_info in products_in_cart.values())


    line_items = []

    for product_id, product_info in products_in_cart.items():
        product = Order.objects.get(id=product_id)

        line_item = {
            'price_data': {
                'currency': 'eur',
                'unit_amount': int(product.product.price * 100),
                'product_data': {
                    'name': product.title,
                    'description': product.description,
                },
            },
            
            'quantity': product_info['quantity'],
        }
        line_items.append(line_item)

    try:
        checkout_session = stripe.checkout.Session.create(
            success_url=request.build_absolute_uri(reverse('success')),
            cancel_url=request.build_absolute_uri(reverse('cancel')),
            payment_method_types=['card'],
            line_items=line_items,
            phone_number_collection={"enabled": True},
            # billing_address_collection={'required': True},
            # billing_address_collection={"enabled": True},
            mode='payment',
            metadata={
                'user_id': user.id,
                'Product_id': product_id_list
            }
        )

        return JsonResponse({'sessionId': checkout_session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)})

logger = logging.getLogger(__name__)

@csrf_exempt
def stripe_webhook(request):
    if request.method == 'POST':
        endpoint_secret = stripe_endpoint_secret
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

        logger.info("Received webhook event")

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
            logger.info("Webhook event constructed successfully")
        except ValueError as e:
            logger.error(f"ValueError: {e}")
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            logger.error(f"SignatureVerificationError: {e}")
            return HttpResponse(status=400)
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return HttpResponse(status=500)

        if event['type'] == 'checkout.session.completed':
            try:
                session = event['data']['object']
                line_items = stripe.checkout.Session.list_line_items(session.id)
                logger.info(f"Line items retrieved: {line_items}")

                customer_email = session['customer_details']['email']
                product_ids = session['metadata']['Product_id'].split(',')
                user_id = session['metadata']['user_id']
                order_number = session['created']
                amount = session['amount_total']
                quantity_order = line_items.data[0]['quantity']

                buffer = BytesIO()
                p = canvas.Canvas(buffer, pagesize=letter)
                #pdfmetrics.registerFont(TTFont('ArialUnicode', 'arial.ttf'))
                p.setFont("Helvetica", 12)

                company_name = "Erika druka"
                logo_path = CustomDesign.objects.first().image.path
                logo = ImageReader(logo_path)
                p.drawImage(logo, 50, 670, width=100, height=100)

                company_code = "Firmas kods: XXXXXXXX"
                address = "Ielas nosaukums, Pilseta, Valsts, Pasta indekss"
                phone = "Telefona numurs: +1234567890"
                email = "E-pasta adrese: info@example.com"

                p.setFillColorRGB(0, 0, 0)
                p.setFont("Helvetica", 12)
                p.drawString(200, 750, company_name)

                p.setFont("Helvetica", 12)
                p.drawString(200, 730, company_code)
                p.drawString(200, 710, address)
                p.drawString(200, 690, phone)
                p.drawString(200, 670, email)

                order_number_text = f"Pasutijuma numurs: {order_number}"
                product_id_text = f"Produkta ID: {product_ids}"
                user_id_text = f"Lietotaja ID: {user_id}"
                amount_text = f"Pasutijuma cena: {amount / 100} EUR"
                quantity_order_text = f"Pasutijuma daudzums: {quantity_order}"
                thank_you_text = "Paldies, ka ieperkaties pie mums!"

                y_coordinate = 600
                for text in [order_number_text, product_id_text, user_id_text, amount_text, quantity_order_text, thank_you_text]:
                    p.drawString(50, y_coordinate, text)
                    y_coordinate -= 20

                p.save()
                buffer.seek(0)

                subject = 'Paldies ka iegadajaties produktu no musu veikala'
                from_email = 'balticctech@gmail.com'
                to_email = [customer_email]

                text_content = 'Paldies, par pirkumu.'
                html_content = render_to_string('e-mail/thank_you_email.html', {'customer_email': customer_email})
                email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
                email.attach_alternative(html_content, "text/html")

                email.attach('purchase_receipt.pdf', buffer.getvalue(), 'application/pdf')
                email.send()
                logger.info(f"Email sent to {customer_email}")

                purchase = Purchase.objects.create(
                    order_number=order_number,
                    amount=amount / 100,
                    user_id=user_id
                )

                for product_id, item in zip(product_ids, line_items.data):
                    PurchaseProduct.objects.create(
                        purchase=purchase,
                        product_id=product_id,
                        quantity=item['quantity']
                    )
                logger.info("Purchase and PurchaseProduct records created successfully")
            except Exception as e:
                logger.error(f"Error processing checkout.session.completed: {e}")
                return HttpResponse(status=500)

        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)

class SuccessView(TemplateView):
    template_name = 'cart.html'


class CancelledView(TemplateView):
    template_name = 'cart.html'