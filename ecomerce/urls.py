from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


from home import views as page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', page.homepage, name='homepage'),
    path('login/', page.login_view, name='login'),
    path('register/', page.register, name='register'),
    path('logout/', page.logout_view, name='logout'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('contact-us/', page.contact_us, name='contact_us'),
    path('creative-corner/', page.creativecorner, name='creativecorner'),
    path('creative-corner/<str:user>/<int:product_list_id>/', page.detail, name='detail'),
    path('save-rating/', page.save_rating, name='save_rating'),
    path('cart/', page.cart, name='cart'),
    path('cart/add/<int:id>/', page.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', page.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         page.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         page.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', page.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',page.cart_detail,name='cart_detail'),
    path('check_discount_code/',page.check_discount_code, name='check_discount_code'),
    path('account/',page.account, name='account'),
    path('save_user_data/', page.save_user_data, name='save_user_data'),
    path('account/change_password/', page.change_password, name='change_password'),
    path('account/delete_account/', page.delete_profile, name='delete_profile'),
    path('design/<slug:slug>/', page.design, name='design_detail'),
]

urlpatterns += i18n_patterns(
    path('', page.homepage, name='homepage'),
    path('admin/', admin.site.urls),
    path('login/', page.login_view, name='login'),
    path('register/', page.register, name='register'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('contact-us/', page.contact_us, name='contact_us'),
    path('cart/', page.cart, name='cart'),
    path('creative-corner/<str:user>/<int:product_list_id>/', page.detail, name='detail'),
    path('account/',page.account, name='account'),
    path('save_user_data/', page.save_user_data, name='save_user_data'),
    path('account/change_password/', page.change_password, name='change_password'),
    path('design/<slug:slug>/', page.design, name='design_detail'),
)

handler404 = page.handler404
handler500 = page.handler500


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)