from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.utils.translation import gettext as _
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from home.models import user as MyUser
from django.contrib.auth import authenticate, login, logout
from django.template.loader import render_to_string
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView, UpdateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from User_app.forms import (LoginForm, RegistrationForm, ContactForm, PersonalInfoForm, LanguageForm,           CustomPasswordChangeForm, DeleteAccountForm)
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, UpdateView
from User_app.models import ContactMessage, Contact
from home.models import Order
from .forms import RegistrationForm
from .models import EmailVerification
from .forms import EmailVerificationForm
from django.utils.crypto import get_random_string
from home.models import CustomDesign



class LoginView(View):
    form_class = LoginForm
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = kwargs
        return context

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = self.get_context_data(form=form)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        context = self.get_context_data(form=form)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage')
            else:
                messages.error(request, 'Nepareizs e-pasts vai parole.')
        else:
            messages.error(request, 'Lūdzu, pārbaudiet ievadītos datus.')

        return render(request, self.template_name, context)


class RegisterView(FormView):
    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('profile:verify_email')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.set_password(form.cleaned_data['password1'])
        user.save()

        verification_code = get_random_string(length=5)
        EmailVerification.objects.create(user=user, verification_code=verification_code)

        context = {
            'user': user,
            'verification_code': verification_code,
            'company_name': 'ericPrint',
            'primary_color': '#007bff',
            'secondary_color': '#6c757d',
        }

        custom_design = CustomDesign.objects.first()
        if custom_design:
            context['company_logo_url'] = custom_design.image.url

        subject = 'Verifikācijas kods'
        from_email = 'no-reply@ericprint.com'
        to_email = user.email

        text_content = render_to_string('emails/verification_email.txt', context)
        html_content = render_to_string('emails/verification_email.html', context)

        email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        email.attach_alternative(html_content, "text/html")
        email.send()

        messages.success(self.request, 'Jūsu profils ir veiksmīgi reģistrēts. Verifikācijas kods tika nosūtīts uz jūsu e-pastu.')

        self.request.session['user_email'] = user.email

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Lūdzu, pārbaudiet ievadītos datus.')
        return super().form_invalid(form)


class EmailVerificationView(FormView):
    template_name = 'verify_email.html'
    form_class = EmailVerificationForm
    success_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_email = self.request.session.get('user_email')
        context['email'] = user_email
        return context

    def form_valid(self, form):
        code = form.cleaned_data['code']
        user_email = self.request.session.get('user_email')
        try:
            user = MyUser.objects.get(email=user_email)
            verification = EmailVerification.objects.get(user=user, verification_code=code, is_verified=False)
            verification.is_verified = True
            verification.user.is_active = True
            verification.user.save()
            verification.save()
            messages.success(self.request, 'Jūsu e-pasts ir veiksmīgi verificēts.')
            return super().form_valid(form)
        except EmailVerification.DoesNotExist:
            form.add_error('code', 'Nepareizs verifikācijas kods.')
            return self.form_invalid(form)


class ResendVerificationCodeView(View):
    def get(self, request, *args, **kwargs):
        user_email = request.session.get('user_email')
        if user_email:
            try:
                user = MyUser.objects.get(email=user_email)
                verification = EmailVerification.objects.get(user=user)
                verification_code = get_random_string(length=5)
                verification.verification_code = verification_code
                verification.save()

                context = {
                    'user': user,
                    'verification_code': verification_code,
                    'company_name': 'ericPrint',
                    'primary_color': '#007bff',
                    'secondary_color': '#6c757d',
                }

                custom_design = CustomDesign.objects.first()
                if custom_design:
                    context['company_logo_url'] = custom_design.image.url

                subject = 'Verifikācijas kods'
                from_email = 'no-reply@ericprint.com'
                to_email = user_email

                text_content = render_to_string('emails/verification_email.txt', context)
                html_content = render_to_string('emails/verification_email.html', context)

                email = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
                email.attach_alternative(html_content, "text/html")
                email.send()

                messages.success(request, 'Jauns verifikācijas kods tika nosūtīts uz jūsu e-pastu.')
            except MyUser.DoesNotExist:
                messages.error(request, 'Lietotājs ar šo e-pasta adresi neeksistē.')
            except EmailVerification.DoesNotExist:
                messages.error(request, 'Verifikācijas informācija nav atrasta.')
        else:
            messages.error(request, 'Radās kļūda. Lūdzu, mēģiniet vēlreiz.')
        return redirect('profile:verify_email')

def logout_view(request):
    logout(request)
    return redirect('login')

class ContactUsView(View):
    template_name = 'contact.html'

    def get(self, request):
        contacts = Contact.objects.first()
        form = ContactForm()

        if request.user.is_authenticated:
            form.fields['first_name'].initial = request.user.first_name
            form.fields['last_name'].initial = request.user.last_name
            form.fields['email'].initial = request.user.email
            form.fields['phone_number'].initial = request.user.phone_number

        context = {
            'form': form,
            'Contact': contacts
        }
        return render(request, self.template_name, context)

    def post(self, request):
        contacts = Contact.objects.first()
        form = ContactForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            user_message = form.cleaned_data['message']

            contact_message = ContactMessage.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                message=user_message
            )

            subject = 'Ziņojums saņemts'
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [email]
            text_content = 'Paldies, par pirkumu.'

            email_content = render_to_string('e-mail/message_received.html', {'contact_message': contact_message})
            email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
            email.attach_alternative(email_content, "text/html")
            email.send()

            messages.success(request, 'Ziņojums ir veiksmīgi nosūtīts!')
            return redirect('contact_us')
        else:
            messages.error(request, 'Radās kļūda. Lūdzu, pārbaudiet ievadītos datus.')

        context = {
            'form': form,
            'Contact': contacts
        }
        return render(request, self.template_name, context)

class PersonalInfoView(LoginRequiredMixin, UpdateView):
    model = MyUser
    form_class = PersonalInfoForm
    template_name = 'Profile/personal_info_form.html'
    success_url = reverse_lazy('profile:personal_info')

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, _('Your personal information has been updated.'))
        return super().form_valid(form)


class CustomPasswordChangeView(FormView):
    form_class = CustomPasswordChangeForm
    success_url = reverse_lazy('password_change_done')
    template_name = 'Profile/password_change_form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

class DeleteAccountView(LoginRequiredMixin, FormView):
    template_name = 'Profile/delete_account_form.html'
    form_class = DeleteAccountForm
    success_url = reverse_lazy('')

    def form_valid(self, form):
        user = self.request.user
        if form.cleaned_data['password']:
            user.delete()
            messages.success(self.request, _('Your account has been deleted successfully.'))
            return super().form_valid(form)
        return self.form_invalid(form)

class OrderHistoryView(LoginRequiredMixin, TemplateView):
    template_name = 'Profile/order_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_orders'] = Order.objects.filter(user=self.request.user)
        return context
