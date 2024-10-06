from django import forms
from .models import Purchase, GiftCode
from django.utils.translation import gettext as _

class PurchaseForm(forms.ModelForm):
    PERSON_TYPE_CHOICES = [
        ('fiziska', _('Fiziska persona')),
        ('juridiska', _('Juridiska persona')),
    ]

    person_type = forms.ChoiceField(
        choices=PERSON_TYPE_CHOICES,
        widget=forms.RadioSelect,
        initial='fiziska'
    )
    terms_agreement = forms.BooleanField(required=True, label=_("Piekritu noteikumiem"))
    gift_code = forms.CharField(
        required=False,
        label=_("Dāvanu kods"),
        widget=forms.TextInput(attrs={'class': 'bg-input-color w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-main-color'})
    )

    class Meta:
        model = Purchase
        fields = ['person_type', 'full_name', 'phone_number', 'email', 'company_name',
                  'company_registration_number', 'company_vat_number', 'company_address',
                  'comments', 'delivery_method', 'payment_method', 'gift_code']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'bg-input-color w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-main-color'}),
            'phone_number': forms.TextInput(attrs={'class':'bg-input-color w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-main-color'}),
            'email': forms.EmailInput(attrs={'class': 'bg-input-color w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-main-color'}),
            'comments': forms.Textarea(attrs={'class': 'bg-input-color w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-main-color'}),

            'company_name': forms.TextInput(attrs={'class': 'bg-input-color w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-main-color'}),
            'company_registration_number': forms.TextInput(attrs={'class': 'bg-input-color w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-main-color'}),
            'company_vat_number': forms.TextInput(attrs={'class': 'bg-input-color w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-main-color'}),
            'company_address': forms.TextInput(attrs={'class': 'bg-input-color w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-main-color'}),

            'delivery_method': forms.Select(attrs={'class': 'bg-input-color w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-main-color'}),
            'payment_method': forms.Select(attrs={'class': 'bg-input-color w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-main-color'}),

            'terms_agreement': forms.CheckboxInput(attrs={'class': 'focus:outline-none focus:ring-2 focus:ring-main-color'}),
        }
        labels = {
            'company_name': _('Uzņēmuma nosaukums'),
            'company_registration_number': _('Reģistrācijas numurs'),
        }

    def __init__(self, *args, **kwargs):
        super(PurchaseForm, self).__init__(*args, **kwargs)
        self.fields['company_name'].required = False
        self.fields['company_registration_number'].required = False
        self.fields['company_vat_number'].required = False
        self.fields['company_address'].required = False

    def clean_gift_code(self):
        gift_code_str = self.cleaned_data.get('gift_code')
        if gift_code_str:
            try:
                gift_code = GiftCode.objects.get(code=gift_code_str)
                if not gift_code.is_active():
                    raise forms.ValidationError(_("Dāvanu kods nav derīgs vai ir beidzies tā derīguma termiņš."))
                return gift_code_str
            except GiftCode.DoesNotExist:
                raise forms.ValidationError(_("Šāds dāvanu kods nepastāv."))
        return None

    def clean(self):
        cleaned_data = super().clean()
        person_type = cleaned_data.get('person_type')

        if not cleaned_data.get('full_name'):
            self.add_error('full_name', _('Vārds un uzvārds ir obligāts.'))
        if not cleaned_data.get('phone_number'):
            self.add_error('phone_number', _('Telefona numurs ir obligāts.'))
        if not cleaned_data.get('email'):
            self.add_error('email', _('E-pasts ir obligāts.'))

        if person_type == 'juridiska':
            if not cleaned_data.get('company_name'):
                self.add_error('company_name', _('Uzņēmuma nosaukums ir nepieciešams juridiskai personai.'))
            if not cleaned_data.get('company_registration_number'):
                self.add_error('company_registration_number', _('Reģistrācijas numurs ir nepieciešams juridiskai personai.'))
            if not cleaned_data.get('company_vat_number'):
                self.add_error('company_vat_number', _('PVN numurs ir nepieciešams juridiskai personai.'))
            if not cleaned_data.get('company_address'):
                self.add_error('company_address', _('Uzņēmuma adrese ir nepieciešama juridiskai personai.'))

        return cleaned_data
