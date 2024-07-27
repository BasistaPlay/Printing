from django.urls import path, include
from shoping_cart import views as cart
from django.conf.urls.i18n import i18n_patterns

app_name = 'shopping_cart'

urlpatterns = [
    path('', cart.cart, name='cart'),
    path('add/<int:id>/', cart.cart_add, name='cart_add'),
    path('item_clear/<int:id>/', cart.item_clear, name='item_clear'),
    path('item_increment/<int:id>/', cart.item_increment, name='item_increment'),
    path('item_decrement/<int:id>/', cart.item_decrement, name='item_decrement'),
    path('cart_clear/', cart.cart_clear, name='cart_clear'),
    path('cart-detail/', cart.cart_detail, name='cart_detail'),
    path('update_sizes/<int:id>/', cart.update_sizes_view, name='update_sizes'),
]

