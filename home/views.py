from django.shortcuts import render, redirect, get_object_or_404
from home.models import CustomDesign, GiftCode
from Product.models import Rating, Product
from django.utils.translation import gettext as _
from django.http import JsonResponse

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
