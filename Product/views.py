from django.shortcuts import render, get_object_or_404
from Product.models import Product, Rating, Category
from product_details.models import Color, ProductInventory
from design.models import Designs
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from Product.ConvertBase64 import save_base64_image
from design.models import TextList, ImageList
from django.db.models import Sum
import json
from datetime import datetime
from django.http import Http404


class CategoryListView(ListView):
    model = Category
    template_name = 'all_categories.html'
    context_object_name = 'categories'


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'
    context_object_name = 'category'
    slug_field = 'slug'
    slug_url_kwarg = 'category_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object()

        if self.request.user.is_staff:
            products = Product.objects.filter(categories=category)
        else:
            products = Product.objects.filter(categories=category, is_public=True)

        context['products'] = products
        return context

class DesignView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'design.html'
    context_object_name = 'product'
    login_url = '/login/'

    def get_object(self, queryset=None):
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        if not product.is_public and not self.request.user.is_staff:
            raise Http404("Product not found")
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

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

        available_colors = product.inventory.values('color__id', 'color__name', 'color__code').annotate(total_quantity=Sum('quantity')).filter(total_quantity__gt=0)
        context['available_colors'] = available_colors

        context['available_sizes'] = product.inventory.values('size__size').distinct()

        context['adjusted_front_image_coords'] = adjusted_front_image_coords
        context['adjusted_back_image_coords'] = adjusted_back_image_coords

        return context

    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            color_id = request.GET.get('color_id')
            if color_id:
                product = self.get_object()
                sizes = ProductInventory.objects.filter(
                    product=product, color_id=color_id
                ).values('size__size', 'quantity').distinct()

                return JsonResponse({'sizes': list(sizes)})
            else:
                return JsonResponse({'error': 'color_id not provided'}, status=400)
        return super().get(request, *args, **kwargs)


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

        filtered_products = Designs.objects.filter(Q(publish_product=True) & Q(allow_publish=True))

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
        context['star_range'] = range(1, 6)
        return context


class ProductDetailView(DetailView):
    model = Designs
    template_name = 'detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_title = self.kwargs.get('Design_title')
        product = self.get_object()


        return context

    def get_object(self):
        Designs_id = self.kwargs.get('Designs_id')
        return get_object_or_404(Designs, id=Designs_id)


class SaveRatingView(LoginRequiredMixin, View):
    login_url = '/login'

    @method_decorator(require_POST)
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        rating_value = request.POST.get('rating')

        try:
            product = get_object_or_404(Designs, id=product_id)
            rating, created = Rating.objects.get_or_create(user=request.user, design=product)
            rating.stars = rating_value
            rating.save()

            product.update_average_rating()

            return JsonResponse({
                'message': 'Reitings saglabāts datubāzē!',
                'average_rating': product.average_rating
            })
        except Exception as e:
            return JsonResponse({'message': f'Kļūda saglabājot reitingu: {str(e)}'}, status=400)

class SaveDesignView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            product_slug = request.POST.get('product_slug')

            product = get_object_or_404(Product, slug=product_slug)
            publish_product = request.POST.get('publish_product') == 'true'
            product_color_name = request.POST.get('product_color')
            product_title = request.POST.get('product_title')
            front_image_base64 = request.POST.get('front_image')
            back_image_base64 = request.POST.get('back_image')

            product_color = get_object_or_404(Color, name=product_color_name)
            texts = json.loads(request.POST.get('texts'))

            timestamp = datetime.now().strftime('%Y%m%d%H%M%S%f')
            front_image_file = save_base64_image(front_image_base64, f'{product_slug}_{request.user}_{timestamp}_front.png')
            back_image_file = save_base64_image(back_image_base64, f'{product_slug}_{request.user}_{timestamp}_back.png')

            new_design = Designs.objects.create(
                author=request.user,
                product=product,
                publish_product=publish_product,
                product_color=product_color,
                title=product_title,
                front_image=front_image_file,
                back_image=back_image_file,
            )

            print(new_design.id)

            for text_data in texts:
                TextList.objects.create(
                    designs_text=new_design,
                    text=text_data['text'],
                    font=text_data['font_family'],
                    text_size=text_data['font_size'],
                    text_color=text_data['text_color']
                )

            images = json.loads(request.POST.get('images'))
            for image_data in images:
                ImageList.objects.create(designs_images=new_design, image=image_data)

            return JsonResponse({'success': True, 'designs_id': new_design.id})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid request'})