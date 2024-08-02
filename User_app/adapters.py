from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.shortcuts import redirect
from django.urls import reverse

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    print('hello')
    def post_social_login(self, request, sociallogin):
        print('hello')
        user = sociallogin.user
        print(user)
        if not user.username or not user.phone_number:
            redirect_url = reverse('profile:extra_info')
            request.session['redirect_after_login'] = redirect_url
            return redirect(redirect_url)