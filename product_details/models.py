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