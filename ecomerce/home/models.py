from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from colorfield.fields import ColorField

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True, verbose_name=('groups'))
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        verbose_name=('user permissions'),
        help_text=('Specific permissions for this user.'),
    )

    def __str__(self):
        return self.username

class Product(models.Model):
    title = models.CharField(max_length=100, unique=True, blank=False, help_text="Ievadiet produkta nosaukumu.")
    moto = models.CharField(max_length=200, blank=False, help_text="Ievadiet produktam saistīto moto vai saukli.")
    description = models.TextField(blank=False, help_text="Ievadiet detalizētu aprakstu par produktu.")
    image = models.ImageField(upload_to='products/', blank=False, help_text="Ievadiet detalizētu aprakstu par produktu.")
    button_title = models.CharField(max_length=100, blank=False, help_text="Ievadiet pogas nosaukumu.")
    link = models.URLField(blank=True, help_text="Ievadiet saiti, uz kuru vedīs poga (ja nepieciešams).")
    background_color = ColorField(verbose_name='Color', blank=False, help_text="Izvēlieties fona krāsu.")
    background_color_2 = ColorField(verbose_name='Color', blank=False, help_text="Izvēlieties otrā fona krāsu.")
    button_color = ColorField(verbose_name='Color', blank=True, help_text="Izvēlieties pogas fona krāsu.")

    def __str__(self):
        return self.title