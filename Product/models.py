from django.db import models
from django.conf import settings
from colorfield.fields import ColorField
from django.utils.translation import gettext as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Count, Avg
from itertools import cycle
from django.utils.text import slugify
from django.apps import apps


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


class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    design = models.ForeignKey('design.Designs', on_delete=models.CASCADE)
    stars = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        verbose_name = _("Vērtējums")
        verbose_name_plural = _("Vērtējumi")

    @staticmethod
    def get_top_rated_popular_products():
        Designs = apps.get_model('design', 'Designs')
        top_rated_popular_products = Designs.objects.annotate(
            num_ratings=Count('rating'),
            avg_rating=Avg('rating__stars')
        ).order_by('-num_ratings', '-avg_rating')[:3]

        top_three_products = list(top_rated_popular_products)
        if len(top_three_products) < 3:
            return top_three_products

        product_cycle = cycle(top_three_products)
        return [next(product_cycle) for _ in range(3)]

@receiver(post_save, sender=Rating)
def update_product_average_rating(sender, instance, **kwargs):
    product = instance.design
    product.update_average_rating()