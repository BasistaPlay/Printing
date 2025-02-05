from django.shortcuts import render, redirect
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from shoping_cart.cart import Cart
from django.views.decorators.csrf import csrf_exempt
from Product.models import Product
from design.models import Designs
from django.contrib import messages
from django.http import HttpResponse
import json

def cart(request):
    products_with_sizes = []
    return render(request, 'cart/cart.html', {
        'products_with_sizes': products_with_sizes
    })

@csrf_exempt
def cart_add(request, id):
    if request.method == 'GET':
        try:
            product = Designs.objects.get(id=id)
            cart = Cart(request)
            selected_items = request.GET.get('selected_items')

            if selected_items:
                # Parse the selected_items JSON string
                items = json.loads(selected_items)
                sizes = []
                for item in items:
                    sizes.append({
                        'size': item['size_id'],
                        'count': item['quantity']
                    })

                # Add items to the cart
                cart.add(product, quantity=1, sizeCount=len(items), sizes=sizes, product_id=id)

                messages.success(request, _('Prece veiksmīgi pievienota grozam.'), extra_tags='success cart')
                return HttpResponse(status=200)
            else:
                messages.error(request, _('Nav izvēlēti neviens izmērs vai daudzums.'))
                return HttpResponse(status=400)

        except Designs.DoesNotExist:
            messages.error(request, _('Prece nav atrasta.'))
            return HttpResponse(status=400)

    return HttpResponse(status=400)



@login_required(login_url="/login")
def item_clear(request, id):
    cart = Cart(request)
    product_list = Designs.objects.get(id=id)
    cart.remove(product_list)
    return redirect('shopping_cart:cart')

@login_required(login_url="/login")
def item_increment(request, id):
    cart = Cart(request)
    product_list = Designs.objects.get(id=id)
    cart.add(product_list)
    return redirect('shopping_cart:cart')

@login_required(login_url="/login")
def item_decrement(request, id):
    cart = Cart(request)
    product_list = Designs.objects.get(id=id)
    cart.decrement(product_list)
    return redirect('shopping_cart:cart')

@login_required(login_url="/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('shopping_cart:cart')

@login_required(login_url="/login")
def cart_detail(request):
    return render(request, 'cart.html')

def update_sizes_view(request, id):
    if request.method == 'POST':
        size = request.POST.get('size')
        quantity = request.POST.get('quantity')
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)
