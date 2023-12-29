from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.db import models
from colorfield.fields import ColorField
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField

# class User(AbstractUser):
#    phone_number = PhoneNumberField(blank=True, null=True)
#    def __str__(self):
#        return self.username

class Product(models.Model):
    title = models.CharField(_('Virsraksts'), max_length=100, unique=True, blank=False, help_text=_("Ievadiet produkta nosaukumu."))
    image = models.ImageField(_('Bilde'), upload_to='products/', blank=False)
    link = models.URLField(blank=True, help_text=_("Ievadiet saiti, uz kuru vedīs poga (ja nepieciešams)."))
    def __str__(self):
        return self.title

class CustomDesign(models.Model):
    title = models.CharField(_('Virsraksts'), max_length=100)
    description = models.TextField(_('Apraksts'),)
    additional_notes = models.TextField(_('papildu piezīmes'))
    image = models.ImageField(_('Bilde'), upload_to='page/', blank=False)

    def __str__(self):
        return self.title
class ContactMessage(models.Model):
    first_name = models.CharField(_('Vārds'), max_length=100)
    last_name = models.CharField(_('Uzvārds'), max_length=100)
    email = models.EmailField(_('E-pasts'))
    phone_number = models.CharField(_('Telefona numurs'), max_length=15)
    message = models.TextField()
    replied = models.BooleanField(_('Atbildēts'), default=False)
    admin_subject = models.CharField(_('Administrātora virsraksts'), max_length=255, blank=True, null=True)
    admin_message = models.TextField(_('Administrātora vēstule'), blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Contact(models.Model):
    address = models.CharField(_('Adrese'), max_length=255)
    postal_code = models.CharField(_('Pasta indekss'), max_length=20)
    phone_number = models.CharField(_('Telefona numurs'), max_length=15)
    email = models.EmailField(_('E-pasts'))
    twitter_link = models.URLField(blank=True, null=True, verbose_name=_('Twitter saite'))
    facebook_link = models.URLField(blank=True, null=True, verbose_name=_('Facebook saite'))
    instagram_link = models.URLField(blank=True, null=True, verbose_name=_('Instagram saite'))

    def __str__(self):
        return f'Kontaktinformācija: {self.address}, {self.postal_code}, {self.phone_number}, {self.email}'

    class Meta:
        verbose_name = _('Kontaktinformācija')
        verbose_name_plural = _('Kontaktinformācija')
        
        
class user(AbstractUser):
    phone_number = PhoneNumberField(blank=True, null=True)
    def __str__(self):
        return self.username