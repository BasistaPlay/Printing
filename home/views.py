from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, ContactMessage, CustomDesign, Contact, Rating, GiftCode, Color, Size, Order ,TextList, ImageList, Purchase
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from home.models import user as MyUser
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import update_session_auth_hash
import json
from cart.context_processor import cart_total_amount
from django.db.models import Q
from django.core.paginator import Paginator
from home.capcha import FormWithCaptcha
from django.template.loader import render_to_string


def homepage(request):
    products = Product.objects.all()
    custom_designs = CustomDesign.objects.first()
    top_rated_popular_products = Rating.get_top_rated_popular_products()
    return render(request, 'home_page.html', {'products' : products, 'custom_designs' : custom_designs, 'products_top' : top_rated_popular_products})

def login_view(request):
    context = {
        'form': FormWithCaptcha(),
    }

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if 'login_attempts' not in request.session:
            request.session['login_attempts'] = 0
        request.session['login_attempts'] += 1

        if request.session['login_attempts'] >= 3:
            context['show_recaptcha'] = True
        else:
            context['show_recaptcha'] = False

        if context['show_recaptcha'] and 'g-recaptcha-response' not in request.POST:
            messages.error(request, 'Lūdzu, veiciet reCAPTCHA pārbaudi.')
            return render(request, 'login.html', context)

        if not username or not password:
            messages.error(request, 'Lūdzu, ievadiet e-pastu un paroli.')
            return render(request, 'login.html', context)

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'Nepareizs e-pasts vai parole.')

    return render(request, 'login.html', context)

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
    context = {
        'form': FormWithCaptcha(),
        'Contact': contacts
    }
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
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [email]
        text_content = 'Paldies, par pirkumu.'

        email_content = render_to_string('e-mail/message_received.html', context)
        email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
        email.attach_alternative(email_content, "text/html")

        email.send()

        messages.success(request, 'Ziņojums ir veiksmīgi nosūtīts!')

        return render(request, 'contact.html', context)

    return render(request, 'contact.html', context)

def design(request, slug):
    product = Product.objects.get(slug=slug)

    return render(request, 'design.html', {'product': product})


from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def creativecorner(request):
    all_colors = Color.objects.all()
    all_products = Product.objects.all()

    search_query = request.GET.get('search', '')
    product_id = request.GET.get('product_list', '')

    colors = request.GET.get('color', '')
    colors_list = [color.strip() for color in colors.split() if color.strip()]

    filtered_products = Order.objects.filter(Q(publish_product=True) & Q(allow_publish=True))

    if search_query:
        filtered_products = filtered_products.filter(Q(title__icontains=search_query) | Q(author__username__icontains=search_query))

    if product_id:
        filtered_products = filtered_products.filter(product_id=product_id)

    if colors_list:
        filtered_products = filtered_products.filter(product_color__id__in=colors_list)

    paginator = Paginator(filtered_products, 10)

    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'all_colors': all_colors,
        'all_products': all_products,
        'page_obj': page_obj,
    }
    return render(request, 'creativecorner.html', context)


def detail(request, user, order_id, product_title):
    product = get_object_or_404(Order, id=order_id)
    size = get_object_or_404(Product, title=product_title)
    return render(request, 'detail.html', {'product': product, 'size':size})

@login_required(login_url="/login")
@require_POST
def save_rating(request):
    product_id = request.POST.get('product_id')
    rating_value = request.POST.get('rating')
    product = get_object_or_404(Order, id=product_id)
    rating, created = Rating.objects.get_or_create(user=request.user, order_id=product_id)

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

def cart_add(request, id):
    cart = Cart(request)
    product_list = Order.objects.get(id=id)
    cart.add(product_list)
    cart_count = len(request.session.get('cart', {}))
    return JsonResponse({'success': True, 'cart_count': cart_count, 'message': 'Product added to cart successfully'})

@login_required(login_url="/login")
def item_clear(request, id):
    cart = Cart(request)
    product_list = Order.objects.get(id=id)
    cart.remove(product_list)
    cart_total = cart_total_amount(request)
    total_amount = cart_total.get('cart_total_amount', 0)
    cart_count = len(request.session.get('cart', {}))
    return JsonResponse({'success': True, 'total_amount': total_amount,'cart_count': cart_count, 'message': 'Product removed from cart successfully'})

@login_required(login_url="/login")
def item_increment(request, id):
    cart = Cart(request)
    product_list = Order.objects.get(id=id)
    cart.add(product_list)
    cart_items = request.session['cart'][f'{id}']['quantity']
    cart_total = cart_total_amount(request)
    total_amount = cart_total.get('cart_total_amount', 0)
    return JsonResponse({'success': True, 'quantity': cart_items,'total_amount': total_amount, 'message': 'Product quantity incremented successfully'})

@login_required(login_url="/login")
def item_decrement(request, id):
    cart = Cart(request)
    product_list = Order.objects.get(id=id)
    cart.decrement(product_list)
    cart_items = request.session['cart'][f'{id}']['quantity']
    cart_total = cart_total_amount(request)
    total_amount = cart_total.get('cart_total_amount', 0)
    return JsonResponse({'success': True, 'quantity': cart_items,'total_amount': total_amount, 'message': 'Product quantity decremented successfully'})

@login_required(login_url="/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return JsonResponse({'success': True, 'message': 'Cart cleared successfully'})

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
    user_orders = Purchase.objects.filter(user=request.user)
    return render(request, 'account.html', {'user_orders': user_orders})

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


@login_required
@csrf_exempt
def save_order(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_slug = request.POST.get('product_slug')
        
        product = get_object_or_404(Product, slug=product_slug)

        publish_product = request.POST.get('publish_product') == 'true'
        product_amount = request.POST.get('num_value')
        product_color_name = request.POST.get('product_color')
        product_size_name = request.POST.get('product_size')
        product_title = request.POST.get('product_title')
        product_description = request.POST.get('product_description')
        front_image_base64 = request.POST.get('front_image')
        back_image_base64 = request.POST.get('back_image')

        product_size = None
        if product_size_name != 'undefined':
            product_size = get_object_or_404(Size, size=product_size_name)

        product_color = get_object_or_404(Color, name=product_color_name)

        texts = json.loads(request.POST.get('texts'))

        new_order = Order.objects.create(
            author=request.user,
            product=product,
            publish_product=publish_product,
            product_amount=int(product_amount),
            product_color=product_color,
            product_size=product_size,
            title=product_title,
            description=product_description,
            front_image=front_image_base64,
            back_image=back_image_base64,
        )

        for text_data in texts:
            text_obj = TextList.objects.create(
                order_text=new_order,
                text=text_data['text'],
                font=text_data['font_family'],
                text_size=text_data['font_size'],
                text_color=text_data['text_color']
            )

        images = json.loads(request.POST.get('images'))
        for image_data in images:
            ImageList.objects.create(order_images=new_order, image=image_data)

        return JsonResponse({'success': True, 'order_id': new_order.id})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request'})