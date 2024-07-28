from django.contrib.auth.models import AbstractUser, Group, Permission, User
from User_app.models import user
from django.db import models
from colorfield.fields import ColorField
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.conf import settings
from django.db.models import Count, Avg
from itertools import cycle
from django.utils.text import slugify

class Category(models.Model):
    title = models.CharField(_('Virsraksts'), max_length=100, unique=True, blank=False, help_text=_("Ievadiet kategorijas nosaukumu."))
    slug = models.SlugField(_('Slug'), unique=True, help_text=_("Ievadiet URL draudzīgu nosaukumu."), blank=True)
    image = models.ImageField(_('Bilde'), upload_to='category_images/', blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Kategorija")
        verbose_name_plural = _("Kategorijas")

class Product(models.Model):
    title = models.CharField(_('Virsraksts'), max_length=100, unique=True, blank=False, help_text=_("Ievadiet produkta nosaukumu."))
    image = models.ImageField(_('Bilde'), upload_to='products/', blank=False)
    slug = models.SlugField(_('Slug'), unique=True, help_text=_("Ievadiet URL draudzīgu nosaukumu."), blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    options = models.TextField(blank=True, help_text=_("Ievadiet opcijas kā sarakstu ar komatiem"))

    front_image_with_background = models.ImageField(_('Priekšējā bilde ar fonu'), upload_to='products/', blank=True)
    front_image_not_background = models.ImageField(_('Priekšējā bilde bez fona'), upload_to='products/', blank=True)
    back_image_with_background = models.ImageField(_('Aizmugurējā bilde ar fonu'), upload_to='products/', blank=True)
    back_image_not_background = models.ImageField(_('Aizmugurējā bilde bez fona'), upload_to='products/', blank=True)

    available_colors = models.ManyToManyField('Color', related_name='products', blank=True)
    available_sizes = models.ManyToManyField('Size', related_name='products', blank=True)

    front_image_coords = models.JSONField(blank=True, null=True)
    back_image_coords = models.JSONField(blank=True, null=True)

    views = models.PositiveIntegerField(default=0)

    categories = models.ManyToManyField(Category, related_name='products')

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
    front_image = models.ImageField(upload_to='designs/', blank=True)
    back_image = models.ImageField(upload_to='designs/', blank=True)
    product_color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    average_rating = models.FloatField(default=0)

    def update_average_rating(self):
        ratings = Rating.objects.filter(order=self)
        if ratings.exists():
            self.average_rating = ratings.aggregate(models.Avg('stars'))['stars__avg']
        else:
            self.average_rating = 0
        self.save()


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


class Rating(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    stars = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        verbose_name = _("Vērtējums")
        verbose_name_plural = _("Vērtējumi")

    @staticmethod
    def get_top_rated_popular_products():
        top_rated_popular_products = Order.objects.annotate(
            num_ratings=Count('rating'),
            avg_rating=Avg('rating__stars')
        ).order_by('-num_ratings', '-avg_rating')[:3]  # Limit the query to top 3 products

        top_three_products = list(top_rated_popular_products)
        if len(top_three_products) < 3:
            return top_three_products  # Return as many products as available

        product_cycle = cycle(top_three_products)
        return [next(product_cycle) for _ in range(3)]

@receiver(post_save, sender=Rating)
def update_product_average_rating(sender, instance, **kwargs):
    product = instance.order
    product.update_average_rating()

class Purchase(models.Model):
    ORDER_STATUS_CHOICES = [
        ('PENDING', _('Gaida apstiprinājumu')),
        ('PROCESSING', _('Apstrāde')),
        ('SHIPPED', _('Nosūtīts')),
        ('DELIVERED', _('Piegādāts')),
        ('CANCELLED', _('Atcelts')),
    ]
    order_number = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order {self.order_number} by {self.user.username}"


class PurchaseProduct(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name='purchase_products')
    product = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.title} - {self.quantity}"