from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.db import models
from colorfield.fields import ColorField
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class user(AbstractUser):
    phone_number = PhoneNumberField(blank=True, null=True)
    def __str__(self):
        return self.username

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


class Price(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.URLField(blank=True)
    options = models.TextField(blank=True, help_text="Ievadiet opcijas kā sarakstu ar komatiem")

    def get_options_list(self):
        return [option.strip() for option in self.options.split(',')]

    def __str__(self):
        return self.title
    
class Product_list(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    front_image = models.ImageField(upload_to='product_images/front/')
    back_image = models.ImageField(upload_to='product_images/back/')
    author = models.ForeignKey(user, on_delete=models.CASCADE)
    price = models.ForeignKey(Price, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    average_rating = models.FloatField(default=0)

    def update_average_rating(self):
        ratings = Rating.objects.filter(product=self)
        if ratings.exists():
            self.average_rating = ratings.aggregate(models.Avg('stars'))['stars__avg']
        else:
            self.average_rating = 0
        self.save()

    def __str__(self):
        return self.title

class Rating(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    product = models.ForeignKey(Product_list, on_delete=models.CASCADE)
    stars = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])

@receiver(post_save, sender=Rating)
def update_product_average_rating(sender, instance, **kwargs):
    product = instance.product
    product.update_average_rating()