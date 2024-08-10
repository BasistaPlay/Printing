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

def cart(request):
    cart_items = request.session.get('cart', {})
    print(cart_items)
    products_with_sizes = []

    try:
        for item_key, item_data in cart_items.items():
            if isinstance(item_data, dict):
                try:
                    design_id = item_data.get('design_id')
                    order_id = item_data.get('product_id')
                    product = get_object_or_404(Product, id=design_id)
                    sizes = product.available_sizes.all()

                    products_with_sizes.append({
                        'product': product,
                        'sizes': sizes,
                        'Design_id': order_id
                    })
                except Product.DoesNotExist as e:
                    print(f"Product with id {design_id} does not exist: {e}")
            else:
                print(f"Invalid item data found in cart session: {item_data}")

    except TypeError as e:
        print(f"Error processing cart items: {e}")

    return render(request, 'cart.html', {
        'products_with_sizes': products_with_sizes
    })

@csrf_exempt
def cart_add(request, id):
    cart = Cart(request)
    product_list = Designs.objects.get(id=id)
    size_data = request.POST.getlist('sizes[]')
    quantity = request.POST.getlist('quantity')
    product_id = int(request.POST.get('product_id', 1))
    sizeCount = int(request.POST.get('sizeCount', 1))
    sizes = [json.loads(size) for size in size_data]

    if len(quantity) > 0:
        quantity = int(quantity[0])
    else:
        quantity = 1

    cart.add(product_list, sizeCount=sizeCount, sizes=sizes, quantity=quantity, product_id=product_id)
    print(request.session.get('cart', {}))
    cart_count = len(request.session.get('cart', {}))
    return JsonResponse({'success': True, 'cart_count': cart_count, 'message': 'Product added to cart successfully'})


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