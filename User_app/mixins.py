from django.shortcuts import redirect
from django.utils.translation import get_language
from django.conf import settings
from django.contrib.auth.mixins import AccessMixin

class CustomLoginRequiredMixin(AccessMixin):
    def handle_no_permission(self):
        lang = get_language() or 'en'
        login_url = settings.LOGIN_URL
        if not login_url.startswith('/'):
            login_url = '/' + login_url
        redirect_url = f'/{lang}{login_url}'
        return redirect(redirect_url)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
