from django.urls import path
from Product import views as product

app_name = 'product'

urlpatterns = [
    path('creative-corner/', product.CreativeCornerView.as_view(), name='creativecorner'),
    path("creative-corner/filter/", product.FilteredCreativeCornerView.as_view(), name="filtered_creative_corner"),
    path('creative-corner/<str:user>/<str:product_title>/<int:Designs_id>/', product.ProductFastView.as_view(), name='detail'),
    path('creative-corner/detail/<str:user>/<str:product_title>/<int:Designs_id>/', product.ProductDetailView.as_view(), name='detail-view'),
    path("rate/<int:design_id>/", product.RateDesignView.as_view(), name="rate-design"),
    path('design/<slug:slug>/', product.DesignView.as_view(), name='design_detail'),
    path('product/<slug:slug>/sizes/', product.LoadSizesView.as_view(), name='load_sizes'),
    path('all-categories/', product.CategoryListView.as_view(), name='all_categories'),
    path('category/<slug:category_slug>/', product.CategoryDetailView.as_view(), name='category_detail'),
    path('save_design/', product.SaveDesignView.as_view(), name='design_save'),
]