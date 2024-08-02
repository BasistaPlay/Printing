from django.urls import path, include
from User_app import views as user
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import views as auth_views

app_name = 'profile'

urlpatterns = [
    path('', user.PersonalInfoView.as_view(), name='personal_info'),
    path('login/', user.LoginView.as_view(), name='login'),
    path('register/', user.RegisterView.as_view(), name='register'),
    path('verify-email/', user.EmailVerificationView.as_view(), name='verify_email'),
    path('resend-verification-code/', user.ResendVerificationCodeView.as_view(), name='resend_verification_code'),
    path('logout/', user.logout_view, name='logout'),
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('contact-us/', user.ContactUsView.as_view(), name='contact_us'),
    path('change_password/', PasswordChangeView.as_view(), name='change_password'),
    path('accounts/', include('allauth.urls')),
    path('accounts/', include('allauth.socialaccount.urls')),
    path('delete-account/', user.DeleteAccountView.as_view(), name='delete_account'),
    path('order-history/', user.PurchaseHistoryView.as_view(), name='order_history'),
    path('password/change/', user.CustomPasswordChangeView.as_view(), name='change_password'),
    path('extra_info/', user.ExtraInfoView.as_view(), name='extra_info'),
]