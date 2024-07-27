from django.shortcuts import render, redirect, get_object_or_404
from home.models import Product, CustomDesign, Rating, GiftCode, Color, Size, Order ,TextList, ImageList, Purchase, Category
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from home.models import user as MyUser
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import update_session_auth_hash, authenticate, login, logout
import json
from django.db.models import Q
from django.core.paginator import Paginator
from home.forms import LoginForm, RegistrationForm, ContactForm, UserProfileForm
from django.template.loader import render_to_string
from home.ConvertBase64 import save_base64_image
from django.views import View
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView

def homepage(request):
    products = Product.objects.all()
    custom_designs = CustomDesign.objects.first()
    top_rated_popular_products = Rating.get_top_rated_popular_products()
    popular_products = Product.objects.order_by('-views')[:2]

    context = {
        'custom_designs': custom_designs,
        'popular_products': popular_products,
        'products' : products,
        'products_top': top_rated_popular_products,
    }

    return render(request, 'home_page.html', context)

def all_categories(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'all_categories.html', context)

def category_detail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(categories=category)
    context = {'category': category, 'products': products}
    return render(request, 'category_detail.html', context)

@login_required(login_url="/login")
def design(request, slug):
    product = get_object_or_404(Product, slug=slug)
    product.views += 1
    product.save()

    front_image_coords = product.front_image_coords
    back_image_coords = product.back_image_coords

    adjusted_front_image_coords = {
        'left': '{:.2f}'.format(front_image_coords['left'] + 15),
        'top': '{:.2f}'.format(front_image_coords['top'] + 20),
        'width': '{:.2f}'.format(front_image_coords['width'] + 35),
        'height': '{:.2f}'.format(front_image_coords['height'] + 20)
    }
    adjusted_back_image_coords = {
        'left': '{:.2f}'.format(back_image_coords['left'] + 15),
        'top': '{:.2f}'.format(back_image_coords['top'] + 20),
        'width': '{:.2f}'.format(back_image_coords['width'] + 35),
        'height': '{:.2f}'.format(back_image_coords['height'] + 20)
    }

    context = {
        'product': product,
        'adjusted_front_image_coords': adjusted_front_image_coords,
        'adjusted_back_image_coords': adjusted_back_image_coords
    }

    return render(request, 'design.html', context)


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

# def account(request):
#     user_orders = Purchase.objects.filter(user=request.user)
#     return render(request, 'account.html', {'user_orders': user_orders})

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


from datetime import datetime

def save_order(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product_slug = request.POST.get('product_slug')

        product = get_object_or_404(Product, slug=product_slug)
        publish_product = request.POST.get('publish_product') == 'true'
        product_color_name = request.POST.get('product_color')
        product_title = request.POST.get('product_title')
        product_description = request.POST.get('product_description')
        front_image_base64 = request.POST.get('front_image')
        back_image_base64 = request.POST.get('back_image')

        product_color = get_object_or_404(Color, name=product_color_name)
        texts = json.loads(request.POST.get('texts'))

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
        front_image_file = save_base64_image(front_image_base64, f'{product_slug}_{request.user}_{timestamp}_front.png')
        back_image_file = save_base64_image(back_image_base64, f'{product_slug}_{request.user}_{timestamp}_back.png')


        new_order = Order.objects.create(
            author=request.user,
            product=product,
            publish_product=publish_product,
            product_color=product_color,
            title=product_title,
            description=product_description,
            front_image=front_image_file,
            back_image=back_image_file,
        )

        for text_data in texts:
            TextList.objects.create(
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