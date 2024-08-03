from django.shortcuts import render, redirect, get_object_or_404
from home.models import Product, CustomDesign, Rating, GiftCode, Color, Order ,TextList, ImageList
from django.utils.translation import gettext as _
from django.http import JsonResponse
import json
from home.ConvertBase64 import save_base64_image

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