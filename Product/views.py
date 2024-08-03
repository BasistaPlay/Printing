from django.shortcuts import render, get_object_or_404
from Product.models import Product, Rating, Color, Category
from home.models import Order
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic import ListView, DetailView

class CategoryListView(ListView):
    model = Category
    template_name = 'all_categories.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'
    slug_field = 'slug'  # Nodrošina, ka tiek izmantots slug kā identificētājs
    slug_url_kwarg = 'category_slug'  # Nodrošina, ka URL konfigurācijā tiek izmantots šis nosaukums

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()
        products = Product.objects.filter(categories=category)
        context['products'] = products
        return context

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

class CreativeCornerView(ListView):
    template_name = 'creativecorner.html'
    context_object_name = 'page_obj'
    paginate_by = 10

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        product_id = self.request.GET.get('product_list', '')
        colors = self.request.GET.get('color', '')
        rating = self.request.GET.get('rating', '')

        colors_list = [color.strip() for color in colors.split() if color.strip()]

        filtered_products = Order.objects.filter(Q(publish_product=True) & Q(allow_publish=True))

        if search_query:
            filtered_products = filtered_products.filter(
                Q(title__icontains=search_query) | Q(author__username__icontains=search_query)
            )

        if product_id:
            filtered_products = filtered_products.filter(product_id=product_id)

        if colors_list:
            filtered_products = filtered_products.filter(product_color__id__in=colors_list)

        if rating:
            filtered_products = filtered_products.filter(average_rating__gte=rating)

        return filtered_products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_colors'] = Color.objects.all()
        context['all_products'] = Product.objects.all()
        context['ratings'] = range(1, 6)  # Assuming rating is from 1 to 5
        return context


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

