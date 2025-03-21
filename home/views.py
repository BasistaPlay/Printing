from django.shortcuts import render
from home.models import CustomDesign
from Product.models import Rating, Product
from User_app.models import FAQ
from django.utils.translation import gettext as _
import os
import re
from django.views.generic import TemplateView, View
from django.templatetags.static import static

class HomePageView(TemplateView):
    template_name = 'home/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['faqs'] = FAQ.objects.all()
        context['custom_designs'] = CustomDesign.objects.first()
        context['products_top'] = Rating.get_top_rated_popular_products()
        context['popular_products'] = Product.objects.filter(is_public=True).order_by('-views')[:20]
        return context

class Handler404View(TemplateView):
    template_name = "error/404.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['error_code'] = 404
        context['error_description'] = "The Page can't be found"
        return context

class Handler500View(TemplateView):
    template_name = "error/404.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['error_code'] = 500
        context['error_description'] = "An internal server error occurred. Please try again later."
        return context