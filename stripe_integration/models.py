from django.db import models

class StripeKeys(models.Model):
    public_key = models.CharField(max_length=300)
    secret_key = models.CharField(max_length=300)
    endpoint_secret = models.CharField(max_length=300)
