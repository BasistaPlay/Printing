from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from shoping_cart.cart import Cart
from django.views.decorators.csrf import csrf_exempt
import json
from Product.models import Product
from shoping_cart.context_processor import cart_total_amount
from design.models import Designs
from django.contrib import messages

def cart(request):
    cart_items = request.session.get('cart', {})
    print(cart_items)
    products_with_sizes = []
    # cart = Cart(request)
    # cart.clear()

    return render(request, 'cart.html', {
        'products_with_sizes': products_with_sizes
    })

@csrf_exempt
def cart_add(request, id):
    if request.method == 'POST':
        try:
            product_list = Designs.objects.get(id=id)
            cart = Cart(request)
            cart.add(product_list)

            messages.success(request, _('Prece veiksmīgi pievienota grozam.'), extra_tags='success cart')
            return JsonResponse({
                'success': True,
                'messages': [m.message for m in messages.get_messages(request)]
            })
        except Designs.DoesNotExist:
            messages.error(request, _('Prece nav atrasta.'))
            return JsonResponse({
                'success': False,
                'messages': [m.message for m in messages.get_messages(request)]
            })

    return JsonResponse({
        'success': False,
        'messages': [_('Nederīgs pieprasījums.')]
    })

@login_required(login_url="/login")
def item_clear(request, id):
    cart = Cart(request)
    product_list = Designs.objects.get(id=id)
    cart.remove(product_list)
    cart_total = cart_total_amount(request)
    total_amount = cart_total.get('cart_total_amount', 0)
    cart_count = len(request.session.get('cart', {}))
    return JsonResponse({'success': True, 'total_amount': total_amount,'cart_count': cart_count, 'message': 'Product removed from cart successfully'})

@login_required(login_url="/login")
def item_increment(request, id):
    cart = Cart(request)
    product_list = Designs.objects.get(id=id)
    cart.add(product_list)
    cart_items = request.session['cart'][f'{id}']['quantity']
    cart_total = cart_total_amount(request)
    total_amount = cart_total.get('cart_total_amount', 0)
    return JsonResponse({'success': True, 'quantity': cart_items,'total_amount': total_amount, 'message': 'Product quantity incremented successfully'})

@login_required(login_url="/login")
def item_decrement(request, id):
    cart = Cart(request)
    product_list = Designs.objects.get(id=id)
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

def update_sizes_view(request, id):
    if request.method == 'POST':
        # Process the request data here
        size = request.POST.get('size')
        quantity = request.POST.get('quantity')

        # Your logic to update the cart goes here

        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)