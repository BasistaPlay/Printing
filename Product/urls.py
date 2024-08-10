from django.urls import path
from Product import views as product

app_name = 'product'

urlpatterns = [
    path('creative-corner/', product.CreativeCornerView.as_view(), name='creativecorner'),
    path('creative-corner/<str:user>/<str:product_title>/<int:order_id>/', product.ProductDetailView.as_view(), name='detail'),
    path('save-rating/', product.SaveRatingView.as_view(), name='save_rating'),
    path('design/<slug:slug>/', product.DesignView.as_view(), name='design_detail'),
    path('all-categories/', product.CategoryListView.as_view(), name='all_categories'),
    path('category/<slug:category_slug>/', product.CategoryDetailView.as_view(), name='category_detail'),
    path('save_design/', product.SaveDesignView.as_view(), name='design_save'),
]