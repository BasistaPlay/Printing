from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone
from django.conf import settings

class CustomDesign(models.Model):
    title = models.CharField(_('Virsraksts'), max_length=100)
    description = models.TextField(_('Apraksts'))
    additional_notes = models.TextField(_('Papildu piezīmes'))
    image = models.ImageField(_('Bilde'), upload_to='page/', blank=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Pielāgots dizains")
        verbose_name_plural = _("Pielāgoti dizaini")


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

    class Meta:
        verbose_name = _("Dāvanu kods")
        verbose_name_plural = _("Dāvanu kodi")


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

    def __str__(self):
        return f"Order {self.order_number} by {self.user.username}"


class PurchaseProduct(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='purchase_products')
    product = models.ForeignKey('Product.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.title} - {self.quantity}"
