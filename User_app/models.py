from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext as _

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

    class Meta:
        verbose_name = _("Kontaktziņojums")
        verbose_name_plural = _("Kontaktziņojumi")


class user(AbstractUser):
    phone_number = PhoneNumberField()
    email = models.EmailField(unique=True)
    agreed_to_terms = models.BooleanField(default=False)
    wants_promotions = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _("Lietotājs")
        verbose_name_plural = _("Lietotāji")


class Contact(models.Model):
    address = models.CharField(_('Adrese'),blank=True, null=True, max_length=255)
    postal_code = models.CharField(_('Pasta indekss'),blank=True, null=True, max_length=20)
    phone_number = models.CharField(_('Telefona numurs'),blank=True, null=True, max_length=15)
    email = models.EmailField(_('E-pasts'), blank=True, null=True,)
    twitter_link = models.URLField(blank=True, null=True, verbose_name=_('Twitter saite'))
    facebook_link = models.URLField(blank=True, null=True, verbose_name=_('Facebook saite'))
    instagram_link = models.URLField(blank=True, null=True, verbose_name=_('Instagram saite'))

    def __str__(self):
        return f'Kontaktinformācija: {self.address}, {self.postal_code}, {self.phone_number}, {self.email}'

    class Meta:
        verbose_name = _("Kontakts")
        verbose_name_plural = _("Kontakti")

class EmailVerification(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class FAQ(models.Model):
    question = models.CharField(max_length=255, verbose_name=_("Jautājums"))
    answer = models.TextField(verbose_name=_("Atbilde"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Izveidots"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Atjaunots"))

    class Meta:
        ordering = ['created_at']
        verbose_name = _("Biežāk uzdoto jautājumu")
        verbose_name_plural = _("Biežāk uzdoto jautājumi")

    def __str__(self):
        return self.question