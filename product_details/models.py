from django.db import models
from colorfield.fields import ColorField
from django.utils.translation import gettext as _


class Color(models.Model):
    name = models.CharField(max_length=100)
    code = ColorField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Krāsa")
        verbose_name_plural = _("Krāsas")


class Size(models.Model):
    name = models.CharField(max_length=100)
    size = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Izmērs")
        verbose_name_plural = _("Izmēri")


class ProductInventory(models.Model):
    product = models.ForeignKey('Product.Product', on_delete=models.CASCADE, related_name='inventory')
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        size_display = self.size.name if self.size else "N/A"
        return f"{self.product.title} - {self.color.name} - {size_display} ({self.quantity} available)"

    class Meta:
        verbose_name = _("Noliktavas krājums")
        verbose_name_plural = _("Noliktavas krājumi")
        constraints = [
            models.UniqueConstraint(fields=['product', 'color', 'size'], name='unique_inventory_item', condition=models.Q(size__isnull=False)),
            models.UniqueConstraint(fields=['product', 'color'], name='unique_inventory_item_without_size', condition=models.Q(size__isnull=True))
        ]