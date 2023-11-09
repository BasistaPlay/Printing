from django.db import models
from colorfield.fields import ColorField

class Product(models.Model):
    title = models.CharField(max_length=100, unique=True, blank=False)
    moto = models.CharField(max_length=200, blank=False)
    description = models.TextField(blank=False)
    image = models.ImageField(upload_to='products/', blank=False)
    button_title = models.CharField(max_length=100, blank=False)
    link = models.URLField(blank=True)
    background_color = ColorField(verbose_name='Color', blank=False)
    background_color_2 = ColorField(verbose_name='Color', blank=False)
    button_color = ColorField(verbose_name='Color', blank=True)

    def __str__(self):
        return self.title