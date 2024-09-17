from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class BankDetails(models.Model):
    bank_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=255)
    recipient = models.CharField(max_length=255)

    def __str__(self):
        return self.bank_name

class Purchase(models.Model):
    ORDER_STATUS_CHOICES = [
        ('PENDING', _('Gaida apstiprinājumu')),
        ('PROCESSING', _('Apstrāde')),
        ('SHIPPED', _('Nosūtīts')),
        ('DELIVERED', _('Piegādāts')),
        ('CANCELLED', _('Atcelts')),
    ]
    order_number = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(default=timezone.now)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.order_number} by {self.user.username}"

class PurchaseProduct(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='purchase_products')
    product = models.ForeignKey('design.Designs', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.title} - {self.quantity}"