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
    path('test/', page.test, name='test'),
    path('creative-corner/<str:user>/<int:product_list_id>/', page.detail, name='detail'),
    path('save-rating/', page.save_rating, name='save_rating'),
    path('cart/', page.cart, name='cart'),
]

urlpatterns += i18n_patterns(
    path('', page.homepage, name='homepage'),
    path('login/', page.login_view, name='login'),
    path('register/', page.register, name='register'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('test/', page.test, name='test'),
    path('contact-us/', page.contact_us, name='contact_us'),
    path('cart/', page.cart, name='cart'),
)

handler404 = page.handler404
handler500 = page.handler500


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)