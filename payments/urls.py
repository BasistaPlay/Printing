from django.urls import path
from payments import views as payment

app_name = 'payments'

urlpatterns = [
    path('bank-details/', payment.BankDetailsView.as_view(), name='bank_details'),
    path('payment-confirmation/', payment.PaymentConfirmationView.as_view(), name='payment_confirmation'),
    path('cancel-purchase/', payment.CancelPurchaseView.as_view(), name='cancel_purchase'),
]