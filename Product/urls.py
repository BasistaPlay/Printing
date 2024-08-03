from django.urls import path
from Product import views as product

app_name = 'product'

urlpatterns = [
    path('creative-corner/', product.CreativeCornerView.as_view(), name='creativecorner'),
    path('creative-corner/<str:user>/<str:product_title>/<int:order_id>/', product.detail, name='detail'),
    path('save-rating/', product.save_rating, name='save_rating'),
    path('design/<slug:slug>/', product.design, name='design_detail'),
    path('all-categories/', product.CategoryListView.as_view(), name='all_categories'),
    path('category/<slug:category_slug>/', product.CategoryDetailView.as_view(), name='category_detail'),

]