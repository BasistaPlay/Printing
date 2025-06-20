from django.db import models
from django.conf import settings
from django.utils.translation import gettext as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Count, Avg, Q
from itertools import cycle
from django.utils.text import slugify
from django.apps import apps
from datetime import datetime
from product_details.models import Color, Size, ProductInventory


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

    front_image_coords = models.JSONField(blank=True, null=True)
    back_image_coords = models.JSONField(blank=True, null=True)

    views = models.PositiveIntegerField(default=0)
    categories = models.ManyToManyField(Category, related_name='products')

    is_public = models.BooleanField(_('Publisks'), default=True, help_text=_("Norādiet, vai produkts ir publisks."))

    can_have_image = models.BooleanField(_('Var ietvert attēlu'), default=False, help_text=_("Norādiet, vai produktā var būt attēls."))
    can_have_text = models.BooleanField(_('Var ietvert tekstu'), default=False, help_text=_("Norādiet, vai produktā var būt teksts."))
    can_have_ai_image = models.BooleanField(_('Var ietvert attēlu ar AI palīdzību'), default=False, help_text=_("Norādiet, vai produktā var būt attēls ar AI palīdzību."))
    can_be_rotate = models.BooleanField(_('Var tikt grozīts'), default=False, help_text=_("Norādiet, vai produktu var apgriezt."))

    def __str__(self):
        return self.title

    def get_options_list(self):
        return [option.strip() for option in self.options.split(',')]

    def get_available_colors(self):
        return Color.objects.filter(productinventory__product=self).distinct()

    def get_available_sizes(self):
        return Size.objects.filter(productinventory__product=self, productinventory__quantity__gt=0).distinct()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = _("Produkts")
        verbose_name_plural = _("Produkti")


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
        Product = apps.get_model('Product', 'Product')

        first_day_of_month = datetime.now().replace(day=1)

        recent_public_products = Designs.objects.filter(
            publish_product=True,
            product__is_public=True,
            created_at__gte=first_day_of_month
        ).annotate(
            num_ratings=Count('rating'),
            avg_rating=Avg('rating__stars')
        ).order_by('-num_ratings', '-avg_rating')[:20]

        if len(recent_public_products) < 20:
            older_public_products = Designs.objects.filter(
                publish_product=True,
                product__is_public=True,
                created_at__lt=first_day_of_month
            ).annotate(
                num_ratings=Count('rating'),
                avg_rating=Avg('rating__stars')
            ).order_by('-num_ratings', '-avg_rating')

            remaining_slots = 20 - len(recent_public_products)
            recent_public_products = list(recent_public_products) + list(older_public_products[:remaining_slots])

        top_products = list(recent_public_products)
        if len(top_products) < 20:
            product_cycle = cycle(top_products)
            return [next(product_cycle) for _ in range(20)]

        return top_products

@receiver(post_save, sender=Rating)
def update_product_average_rating(sender, instance, **kwargs):
    product = instance.design
    product.update_average_rating()