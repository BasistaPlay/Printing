from django.db import models
from django.utils.translation import gettext as _
from django.utils import timezone

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
