from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.db import models
from colorfield.fields import ColorField
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from PIL import Image
from django.conf import settings


class user(AbstractUser):
    phone_number = PhoneNumberField(blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _("Lietotājs")
        verbose_name_plural = _("Lietotāji")


class Product(models.Model):
    title = models.CharField(_('Virsraksts'), max_length=100, unique=True, blank=False, help_text=_("Ievadiet produkta nosaukumu."))
    image = models.ImageField(_('Bilde'), upload_to='products/', blank=False)
    slug = models.SlugField(_('Slug'), unique=True, help_text=_("Ievadiet URL draudzīgu nosaukumu."), blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    options = models.TextField(blank=True, help_text="Ievadiet opcijas kā sarakstu ar komatiem")

    front_image_with_background = models.ImageField(_('Priekšējā bilde ar fonu'), upload_to='products/', blank=True)
    front_image_not_background = models.ImageField(_('Priekšējā bilde bez fona'), upload_to='products/', blank=True)
    back_image_with_background = models.ImageField(_('Aizmugurējā bilde ar fonu'), upload_to='products/', blank=True)
    back_image_not_background = models.ImageField(_('Aizmugurējā bilde bez fona'), upload_to='products/', blank=True)

    available_colors = models.ManyToManyField('Color', related_name='products', blank=True)
    available_sizes = models.ManyToManyField('Size', related_name='products', blank=True)

    def __str__(self):
        return self.title

    def get_options_list(self):
        return [option.strip() for option in self.options.split(',')]

    class Meta:
        verbose_name = _("Produkts")
        verbose_name_plural = _("Produkti")


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


class CustomDesign(models.Model):
    title = models.CharField(_('Virsraksts'), max_length=100)
    description = models.TextField(_('Apraksts'),)
    additional_notes = models.TextField(_('Papildu piezīmes'))
    image = models.ImageField(_('Bilde'), upload_to='page/', blank=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Pielāgots dizains")
        verbose_name_plural = _("Pielāgoti dizaini")


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
        verbose_name = _("Kontakts")
        verbose_name_plural = _("Kontakti")


class Product_list(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    front_image = models.ImageField(upload_to='product_images/front/')
    back_image = models.ImageField(upload_to='product_images/back/')
    author = models.ForeignKey(user, on_delete=models.CASCADE)
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

    class Meta:
        verbose_name = _("Produkta saraksts")
        verbose_name_plural = _("Produktu saraksti")


class Rating(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    product = models.ForeignKey(Product_list, on_delete=models.CASCADE)
    stars = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        verbose_name = _("Vērtējums")
        verbose_name_plural = _("Vērtējumi")


@receiver(post_save, sender=Rating)
def update_product_average_rating(sender, instance, **kwargs):
    product = instance.product
    product.update_average_rating()


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



class Order(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    publish_product = models.BooleanField(default=False)
    allow_publish = models.BooleanField(default=False)
    front_image = models.ImageField(upload_to='users_products/', blank=True)
    back_image = models.ImageField(upload_to='users_products/', blank=True)
    product_color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True)
    product_amount = models.IntegerField(default=0)
    product_size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True)


class TextList(models.Model):
    order_text = models.ForeignKey(Order, on_delete=models.CASCADE)
    text = models.TextField(blank=True)
    font = models.CharField(max_length=50, blank=True)
    text_size = models.CharField(blank=True, max_length=25)
    text_color = models.CharField(max_length=20, blank=True)

class ImageList(models.Model):
    order_images = models.ForeignKey(Order, on_delete=models.CASCADE)
    image = models.TextField(blank=True)

    def __str__(self):
        return f'Image for Order {self.order_images.id}'