from django import forms
from django_recaptcha.fields import ReCaptchaField

class FormWithCaptcha(forms.Form):
    username = forms.CharField(max_length=100, label='Lietotājvārds', required=True)
    password = forms.CharField(max_length=100, label='Parole', required=True, widget=forms.PasswordInput)
    captcha = ReCaptchaField(required=True)