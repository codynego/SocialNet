from django.urls import path
from .views import RegistrationView, LoginView, EmailVerificationView, ResendVerificationEmailView, RequestPasswordResetEmailView, PasswordResetTokenValidationView, SetNewPasswordView, LogoutView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)




urlpatterns = [
    # user registration and login
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    # email verification
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify-email/', EmailVerificationView.as_view(), name = "verify-email"),
    path('resend-verification-email/', ResendVerificationEmailView.as_view(), name = "resend-verification-email"),

    # password reset
    path('request-password-reset-email/', RequestPasswordResetEmailView.as_view(), name='request-password-reset-email'),
    path('password-reset/<uidb64>/<token>/', PasswordResetTokenValidationView.as_view(), name='password-reset-confirm'),
    path('password-reset/', SetNewPasswordView.as_view(), name='password-reset'),

    #logout
    path('logout/', LogoutView.as_view(), name="logout"),
]