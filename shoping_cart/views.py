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
            print(f"Received selected_items: {selected_items}")

            if selected_items:
                items = json.loads(selected_items)

                sizes = [{'size': size_id, 'count': count} for size_id, count in items.items() if count > 0]

                if sizes:
                    cart.add(product, quantity=1, sizeCount=len(sizes), sizes=sizes, product_id=id)

                    # Aizvietojam `cart.get_total_items()` ar pareizo metodi
                    total_items = sum(item['quantity'] for item in cart.session.get('cart', {}).values())

                    return JsonResponse({'cart_count': total_items, 'message': 'Prece veiksmīgi pievienota grozam.'}, status=200)
                else:
                    return JsonResponse({'error': 'Nav izvēlēts neviens derīgs izmērs vai daudzums.'}, status=400)

        except Designs.DoesNotExist:
            return JsonResponse({'error': 'Prece nav atrasta.'}, status=404)

    return JsonResponse({'error': 'Neatbalstīts pieprasījums.'}, status=400)



@login_required(login_url="/login")
def item_clear(request, id):
    size = request.GET.get("size")

    cart = Cart(request)

    if size:  # Ja izmērs ir padots, dzēs specifisku ierakstu ar izmēru
        cart.remove(id, size)
    else:  # Ja izmērs nav padots, dzēs vienkārši pēc produkta ID
        cart.remove(id)

    return redirect("shopping_cart:cart")

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
