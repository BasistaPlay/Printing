from django.urls import path
from payments import views as payment

app_name = 'payments'

urlpatterns = [
    path('', payment.CheckoutView.as_view(), name='payment'),

    path('bank-details/', payment.BankDetailsView.as_view(), name='bank_details'),
    path('payment-confirmation/', payment.PaymentConfirmationBaseView.as_view(), name='payment_confirmation'),
    path('cancel-purchase/', payment.CancelPurchaseView.as_view(), name='cancel_purchase'),

    path('webhook/', payment.StripeWebhookView.as_view(), name='stripe-webhook'),
    path('stripe/checkout/', payment.StripeCheckoutView.as_view(), name='stripe_checkout'),

    path('payment-success/bank-transfer/', payment.BankTransferConfirmationView.as_view(), name='bank_transfer_success'),
    path('payment-success/stripe/', payment.StripePaymentConfirmationView.as_view(), name='stripe_payment_success'),
]
