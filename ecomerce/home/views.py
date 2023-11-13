from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate, login, logout





def homepage(request):
    products = Product.objects.all()
    return render(request, 'home_page.html', {'products': products})

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, _('Nepareizs e-pasts vai parole.'))

    return render(request, 'login.html')

def register(request):
    errors = []
    
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if not phone_number:
            errors.append(_('Lūdzu ievadiet abas paroles.'))
        
        if pass1 != pass2:
            errors.append(_('Paroles nesakrīt.'))
            
        if not first_name or not last_name:
                    errors.append(_('Lūdzu, ievadiet gan vārdu, gan uzvārdu.'))

        if not phone_number:
            errors.append(_('Lūdzu ievadiet telefona numuru.'))
        
        if User.objects.filter(email=email).exists():
            errors.append(_('Šī e-pasta adrese jau tiek izmantota.'))

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'register.html')

        try:
            user = User.objects.create_user(username=email, email=email, password=pass1)
            user.first_name = first_name
            user.last_name = last_name
            user.phone_number = phone_number
            user.save()
            messages.success(request, _('Your profile was successfully registered.'))
            return redirect('login')
        except ValidationError as e:
            messages.error(request, e.message)

    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('login')