from django.db import models
from django.utils.translation import gettext as _
from django.conf import settings
from django.apps import apps
from django.utils import timezone

class Designs(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    publish_product = models.BooleanField(default=False)
    allow_publish = models.BooleanField(default=False)
    front_image = models.ImageField(upload_to='designs/', blank=True)
    back_image = models.ImageField(upload_to='designs/', blank=True)
    product_color = models.ForeignKey('product_details.Color', on_delete=models.CASCADE, null=True)
    product = models.ForeignKey('Product.Product', on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=255, blank=True)
    average_rating = models.FloatField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    @property
    def average_rating(self):
        Rating = apps.get_model('Product', 'Rating')
        result = Rating.objects.filter(design=self).aggregate(avg=models.Avg('stars'))
        return result['avg'] or 0

    class Meta:
        verbose_name = _("Dizaini")
        verbose_name_plural = _("Dizaini")


class TextList(models.Model):
    designs_text = models.ForeignKey(Designs, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    font = models.CharField(max_length=50, blank=True)
    text_size = models.CharField(blank=True, max_length=25)
    text_color = models.CharField(max_length=20, blank=True)

class ImageList(models.Model):
    designs_images = models.ForeignKey(Designs, on_delete=models.CASCADE)
    image = models.TextField(blank=True)

    def __str__(self):
        return f'Image for design {self.designs_images.id}'