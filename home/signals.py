# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.conf import settings
# from django_recaptcha.models import RecaptchaKeys

# @receiver(post_save, sender=RecaptchaKeys)
# def update_settings(sender, instance, **kwargs):
#     update_settings_from_database()

# def update_settings_from_database():
#     try:
#         latest_instance = RecaptchaKeys.objects.latest('id')
#         public_key, private_key = latest_instance.public_key, latest_instance.private_key
#         settings.RECAPTCHA_PUBLIC_KEY = public_key
#         settings.RECAPTCHA_PRIVATE_KEY = private_key
#     except RecaptchaKeys.DoesNotExist:
#         settings.RECAPTCHA_PUBLIC_KEY = None
#         settings.RECAPTCHA_PRIVATE_KEY = None


# update_settings_from_database()
