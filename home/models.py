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
