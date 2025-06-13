from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import uuid
from product_details.models import Size

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
    PAYMENT_METHOD_CHOICES = [
        ('INTERNETBANKA', _('Internetbanka')),
        ('BANK_TRANSFER', _('Bankas pārskaitījums')),
        ('APPLE_PAY', ('Apple Pay')),
        ('STRIPE', ('Stripe')),
    ]
    DELIVERY_CHOICES = [
        ('DPD', ('DPD')),
        ('OMNIVA', ('Omniva')),
        ('PASTS', ('Pasts')),
    ]

    order_number = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Atlaide
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='PENDING')
    is_paid = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='INTERNETBANKA')
    created_at = models.DateTimeField(default=timezone.now)
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default='DPD')

    full_name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_registration_number = models.CharField(max_length=50, blank=True, null=True)
    company_vat_number = models.CharField(max_length=50, blank=True, null=True)
    company_address = models.TextField(blank=True, null=True)

    gift_code = models.CharField(max_length=100, blank=True, null=True)

    def apply_gift_code(self, gift_code):
        if gift_code.is_active() and self.amount >= gift_code.min_order_amount:
            self.discount_amount = gift_code.discount_value
            self.amount = gift_code.apply_discount(self.amount)
            gift_code.use()
            self.save()

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f'ORD-{uuid.uuid4().hex[:6].upper()}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_number} by {self.user.username}"


class PurchaseProduct(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='purchase_products')
    product = models.ForeignKey('design.Designs', on_delete=models.CASCADE)
    size = models.ForeignKey(Size, null=True, blank=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.title} - {self.quantity}"


class GiftCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    is_valid = models.BooleanField(default=True)
    discount_type = models.CharField(max_length=20, choices=[('percentage', 'Percentage'), ('fixed', 'Fixed')])
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    unlimited_usage = models.BooleanField(default=False)

    def __str__(self):
        return self.code

    def is_active(self):
        today = timezone.now().date()
        return (
            self.is_valid and
            (not self.start_date or today >= self.start_date) and
            (not self.end_date or today <= self.end_date) and
            (self.unlimited_usage or self.quantity is None or self.quantity > 0)
        )

    def apply_discount(self, amount):
        if self.discount_type == 'percentage':
            return amount * (1 - (self.discount_value / 100))
        elif self.discount_type == 'fixed':
            return amount - self.discount_value
        return amount

    def use(self):
        if not self.unlimited_usage and self.quantity is not None:
            self.quantity -= 1
            if self.quantity <= 0:
                self.is_valid = False
            self.save()

    class Meta:
        verbose_name = _("Dāvanu kods")
        verbose_name_plural = _("Dāvanu kodi")
