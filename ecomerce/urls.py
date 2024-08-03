from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.i18n import set_language
from django.contrib.auth.views import PasswordChangeView

from home import views as page
from shoping_cart import views as cart
from stripe_integration import views as stripe
from User_app import views as user

urlpatterns = [
     path('admin/', admin.site.urls),
     path('i18n/', include('django.conf.urls.i18n')),
     path('', page.homepage, name='homepage'),
     # path('creative-corner/', page.creativecorner, name='creativecorner'),
     # path('creative-corner/<str:user>/<str:product_title>/<int:order_id>/', page.detail, name='detail'),
     # path('save-rating/', page.save_rating, name='save_rating'),
     path('check_discount_code/',page.check_discount_code, name='check_discount_code'),
     # path('design/<slug:slug>/', page.design, name='design_detail'),
     path('save_order/', page.save_order, name='save_order'),
     # path('all-categories/', page.all_categories, name='all_categories'),
     # path('category/<slug:category_slug>/', page.category_detail, name='category_detail'),
     path('accounts/', include('allauth.urls')),
     path('cart/', include('shoping_cart.urls')),
     path('profile/', include('User_app.urls')),
     path('product/', include('Product.urls')),

]

urlpatterns += i18n_patterns(
     path('', page.homepage, name='homepage'),
     path('admin/', admin.site.urls),
     path('login/', user.LoginView.as_view(), name='login'),
     path('register/', user.RegisterView.as_view(), name='register'),
     path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
     path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
     path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
     path('contact-us/', user.ContactUsView.as_view(), name='contact_us'),
     path('cart/', cart.cart, name='cart'),
     # path('creative-corner/<str:user>/<int:product_list_id>/', page.detail, name='detail'),
     # path('save_user_data/', user.save_user_data, name='save_user_data'),
     # path('account/change_password/', user.change_password, name='change_password'),
     # path('design/<slug:slug>/', page.design, name='design_detail'),
     # path('creative-corner/', page.creativecorner, name='creativecorner'),
     # path('creative-corner/<str:user>/<str:product_title>/<int:order_id>/', page.detail, name='detail'),
     # path('password/change/', user.CustomPasswordChangeView.as_view(), name='change_password'),
     # path('success/', stripe.SuccessView.as_view(), name='success'),
)

handler404 = page.handler404
handler500 = page.handler500


if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
