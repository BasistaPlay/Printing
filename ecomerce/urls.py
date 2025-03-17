from django.contrib import admin
from django.urls import include, path
from django.utils.translation import gettext_lazy as _
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.http import Http404
from django.views.i18n import JavaScriptCatalog

from home import views as home
from User_app import views as user

def admin_required(function):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise Http404("Page not found")
        return function(request, *args, **kwargs)
    return wrapper

urlpatterns = [
     path('admin/', admin.site.urls),
     path('i18n/', include('django.conf.urls.i18n')),
     path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
     path('', home.HomePageView.as_view(), name='homepage'),
     path('sprite-svg/', admin_required(TemplateView.as_view(template_name='sprite_svg_preview.html'))),
     path('accounts/', include('allauth.urls')),
     path('cart/', include('shoping_cart.urls')),
     path('profile/', include('User_app.urls')),
     path('product/', include('Product.urls')),
     path('payments/', include('payments.urls')),
     path('rosetta/', include('rosetta.urls')),
     path('manifest.json', home.manifest, name='manifest'),
]


urlpatterns += i18n_patterns(
     path('', home.HomePageView.as_view(), name='homepage'),
     path('admin/', admin.site.urls),
     path('login/', user.LoginView.as_view(), name='login'),
     path('register/', user.RegisterView.as_view(), name='register'),
     path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
     path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
     path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
     path('contact-us/', user.ContactUsView.as_view(), name='contact_us'),
)

handler404 = home.Handler404View.as_view()
handler500 = home.Handler500View.as_view()


if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
