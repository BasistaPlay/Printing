from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, ContactMessage, CustomDesign, Contact, Product_list, Rating, GiftCode
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from home.models import user as MyUser
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import update_session_auth_hash


def homepage(request):
    products = Product.objects.all()
    custom_designs = CustomDesign.objects.first()
    return render(request, 'home_page.html', {'products' : products, 'custom_designs' : custom_designs})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, _('Lūdzu, ievadiet e-pastu un paroli.'))
            return render(request, 'login.html')

        user = authenticate(request, username=username, password=password)

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
        username = request.POST['username']
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
        
        if MyUser.objects.filter(email=email).exists():
            errors.append(_('Šī e-pasta adrese jau tiek izmantota.'))

        if MyUser.objects.filter(username=username).exists():
            errors.append(_('Šī Lietotājvārds jau tiek izmantots.'))

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'register.html')

        try:
            user = MyUser.objects.create_user(username=username, email=email, password=pass1)
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

        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        phone_number = request.POST.get('phone_number', '')
        user_message = request.POST.get('message', '')

        contact_message = ContactMessage.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            message=user_message
        )

        subject = 'Ziņojums saņemts'
        message = 'Paldies par Jūsu ziņojumu. Mēs esam to saņēmuši un sazināsimies ar Jums drīzumā.'
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [email]

        send_mail(subject, message, from_email, to_email, fail_silently=False)

        messages.success(request, 'Ziņojums ir veiksmīgi nosūtīts!')

        return render(request, 'contact.html', {'Contact': contacts})
    else:

        return render(request, 'contact.html', {'Contact': contacts})

def design(request, slug):
    product = Product.objects.get(slug=slug)

    return render(request, 'design.html', {'product': product})


def creativecorner(request):
    product_list = Product_list.objects.all()
    return render(request, 'creativecorner.html', {'Product_list': product_list})

def detail(request, user, product_list_id):
    product = get_object_or_404(Product_list, id=product_list_id)
    return render(request, 'detail.html', {'product': product})

@login_required(login_url="/login")
@require_POST
def save_rating(request):
    product_id = request.POST.get('product_id')
    rating_value = request.POST.get('rating')

    product = get_object_or_404(Product_list, id=product_id)

    rating, created = Rating.objects.get_or_create(user=request.user, product=product)
    rating.stars = rating_value
    rating.save()

    return JsonResponse({'message': 'Reitings saglabāts datubāzē!'})


def handler404(request, exception):
    error_description = "The Page can't be found"
    context = {
        'error_code': 404,
        'error_description': error_description,
    }
    return render(request, 'error/404.html', context, status=404)

def handler500(request):
    error_description = "An internal server error occurred. Please try again later."
    context = {
        'error_code': 500,
        'error_description': error_description,
    }
    return render(request, 'error/404.html', context, status=500)

@login_required(login_url="/login")
def cart(request):
    return render(request, 'cart.html')

@login_required(login_url="/login")
def cart_add(request, id):
    cart = Cart(request)
    product_list = Product_list.objects.get(id=id)
    cart.add(product_list)
    return redirect("homepage")


@login_required(login_url="/login")
def item_clear(request, id):
    cart = Cart(request)
    product_list = Product.objects.get(id=id)
    cart.remove(product_list)
    return redirect("cart_detail")


@login_required(login_url="/login")
def item_increment(request, id):
    cart = Cart(request)
    product_list = Product.objects.get(id=id)
    cart.add(product_list)
    return redirect("cart_detail")


@login_required(login_url="/login")
def item_decrement(request, id):
    cart = Cart(request)
    product_list = Product.objects.get(id=id)
    cart.decrement(product_list)
    return redirect("cart_detail")


@login_required(login_url="/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")

@login_required(login_url="/login")
def cart_detail(request):
    return render(request, 'cart.html')


def check_discount_code(request):
    if request.method == 'POST':
        discount_code = request.POST.get('discount-token', None)

        if discount_code:
            try:
                gift_code = GiftCode.objects.get(code=discount_code, is_valid=True)
                discount_type = gift_code.discount_type
                discount_value = gift_code.discount_value

                return JsonResponse({'valid': True, 'type': discount_type, 'value': discount_value})
            except GiftCode.DoesNotExist:
                pass

    return JsonResponse({'valid': False})

def account(request):
    return render(request, 'account.html')

def save_user_data(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        username = request.POST.get('username') 

        if email and phone and username:
            existing_email = MyUser.objects.filter(email=email).exclude(username=request.user.username).exists()
            existing_phone = MyUser.objects.filter(phone_number=phone).exclude(username=request.user.username).exists()
            existing_username = MyUser.objects.filter(username=username).exclude(username=request.user.username).exists()

            error_messages = {}

            if existing_email:
                error_messages['email'] = _('E-pasts jau eksistē citam lietotājam')

            if existing_phone:
                error_messages['phone'] = _('Tālruņa numurs jau eksistē citam lietotājam')

            if existing_username:
                error_messages['username'] = _('Lietotājvārds jau eksistē citam lietotājam')
            
            if error_messages:
                return JsonResponse({'success': False, 'errors': error_messages})

            request.user.email = email
            request.user.username = username
            request.user.save()

            user = request.user
            user.phone_number = phone
            user.save()

            return JsonResponse({'success': True, 'email': email, 'phone': phone})
        else:
            return JsonResponse({'success': False, 'error': _('Nederīgi dati')})

    return JsonResponse({'success': False, 'error': _('Nederīga pieprasījuma metode')})


@login_required
@method_decorator(csrf_exempt, name='dispatch')
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('oldPassword')
        new_password = request.POST.get('newPassword')

        if not request.user.check_password(old_password):
            return JsonResponse({'success': False, 'error': _('Vecā parole nav pareiza.')})

        if not is_valid_password(new_password):
            return JsonResponse({'success': False, 'error': _('Jaunā parole neatbilst nosacījumiem.')})

        request.user.set_password(new_password)
        request.user.save()

        update_session_auth_hash(request, request.user)

        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': _('Metode POST ir obligāta.')})

def is_valid_password(password):
    return len(password) >= 8 and any(char.isdigit() for char in password) and any(char.isupper() for char in password)


@login_required
@csrf_exempt
def delete_profile(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        print(password)
        if request.user.check_password(password):
            request.user.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': _('Nepareiza parole.')})
    return JsonResponse({'success': False, 'error': _('Metode POST ir obligāta.')})