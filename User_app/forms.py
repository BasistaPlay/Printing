from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from User_app.models import user
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.phonenumber import PhoneNumber
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = user
        fields = ('username', 'email', 'password1', 'password2', 'phone_number')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class RegistrationForm(UserCreationForm):
    phone_number = PhoneNumberField()
    country_code = forms.CharField(max_length=5, widget=forms.HiddenInput())
    agree_to_terms = forms.BooleanField(required=True, label=_("Piekrītu interneta veikala noteikumiem"))

    class Meta:
        model = user
        fields = ['first_name', 'last_name', 'email', 'username', 'phone_number', 'country_code', 'password1', 'password2', 'agree_to_terms']
        widgets = {
            'password1': forms.PasswordInput(attrs={'placeholder': _('Parole')}),
            'password2': forms.PasswordInput(attrs={'placeholder': _('Apstipriniet paroli')}),
        }
        labels = {
            'phone_number': _('Talruņa numurs'),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Paroles nesakrīt")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if user.objects.filter(email=email).exists():
            raise ValidationError(_("Šī e-pasta adrese jau tiek izmantota."))
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if user.objects.filter(username=username).exists():
            raise ValidationError(_("Šis lietotājvārds jau tiek izmantots."))
        return username

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        country_code = self.cleaned_data.get('country_code')

        if phone_number:
            try:
                full_number = f"{country_code}{phone_number}"
                phone_number_obj = PhoneNumber.from_string(full_number)
                phone_number_obj.as_e164
            except Exception as e:
                raise ValidationError(_(f"Nepareizs telefona numurs: {e}"))

            if user.objects.filter(phone_number=phone_number_obj.as_e164).exists():
                raise ValidationError(_("Šis telefona numurs jau tiek izmantots."))

        return phone_number

class ExtraInfoForm(forms.ModelForm):
    class Meta:
        model = user
        fields = ['username', 'phone_number']

class EmailVerificationForm(forms.Form):
    code = forms.CharField(max_length=5, required=True, label=_('Verifikācijas kods'))


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)
    message = forms.CharField(widget=forms.Textarea)


class PersonalInfoForm(forms.ModelForm):
    class Meta:
        model = user
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'wants_promotions']
        widgets = {
            'first_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'last_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'wants_promotions': forms.CheckboxInput(),
        }
        labels = {
            'phone_number': _('Talruņa numurs'),
        }

    def __init__(self, *args, **kwargs):
        super(PersonalInfoForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if self.errors.get(field_name):
                field.widget.attrs.update({'class': 'is-invalid'})


class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = user
        fields = ('old_password', 'new_password1', 'new_password2')

class DeleteAccountForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label=_('Parole')
    )