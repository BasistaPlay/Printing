from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, ContactMessage, CustomDesign, Contact, Product_list, Rating
from home.models import User
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST
from django.http import JsonResponse



def homepage(request):
    products = Product.objects.all()
    custom_designs = CustomDesign.objects.first()
    return render(request, 'home_page.html', {'products' : products, 'custom_designs' : custom_designs})

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
            messages.success(request, _('Jūsu profils ir veiksmīgi reģistrēts.'))
            return redirect('login')
        except ValidationError as e:
            messages.error(request, e.message)

    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def contact_us(request):
    contacts = Contact.objects.first()
    if request.method == 'POST':
        # Saņemiet datus no POST pieprasījuma
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        phone_number = request.POST.get('phone_number', '')
        user_message = request.POST.get('message', '')

        # Saglabājiet datus datu bāzē
        contact_message = ContactMessage.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            message=user_message
        )

        # Izmantojiet send_mail, lai aizsūtītu apstiprinājuma ziņojumu lietotājam
        subject = 'Ziņojums saņemts'
        message = 'Paldies par Jūsu ziņojumu. Mēs esam to saņēmuši un sazināsimies ar Jums drīzumā.'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [email]

        send_mail(subject, message, from_email, to_email, fail_silently=False)

        # Paziņot lietotājam, ka ziņojums ir veiksmīgi nosūtīts
        messages.success(request, 'Ziņojums ir veiksmīgi nosūtīts!')

        # Neaizmirstiet importēt messages no django.contrib
        return render(request, 'contact.html', {'Contact': contacts})
    else:
        # Jūsu esošais skats kodam šeit
        return render(request, 'contact.html', {'Contact': contacts})
    

def test(request):
    return render(request, 'test.html')


def creativecorner(request):
    product_list = Product_list.objects.all()
    return render(request, 'creativecorner.html', {'Product_list': product_list})

def detail(request, user, product_list_id):
    product = get_object_or_404(Product_list, id=product_list_id)
    return render(request, 'detail.html', {'product': product, 'user': user})


@require_POST
def save_rating(request):
    product_id = request.POST.get('product_id')
    rating_value = request.POST.get('rating')

    # Iegūstiet vai izveidojiet produktu, uz kuru attiecas reitings
    product = get_object_or_404(Product_list, id=product_id)

    # Saglabājiet reitingu datu bāzē
    rating, created = Rating.objects.get_or_create(user=request.user, product=product)
    rating.stars = rating_value
    rating.save()

    return JsonResponse({'message': 'Reitings saglabāts datubāzē!'})