from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import *


app_name = 'apps.authentication'

urlpatterns = [
    path('token/obtain/', ObtainTokenPairWithColorView.as_view(), name='token_create'),
    # override sjwt stock token
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('blacklist/', LogoutAndBlacklistRefreshTokenForUserView.as_view(), name='blacklist'),
    path('register/', RegistrationView.as_view(), name='registration'),
    path('send-message/contact-support/', ContactSupportView.as_view(), name='contact_support'),
    path("activate/<uidb64>/<token>/", Verification.as_view(), name="activate"),
    path('update_user_image/<str:username>/', UpdateImageView.as_view(), name='update_image'),
    path('password_reset_request/', PasswordResetRequest.as_view(), name='password_reset_request'),
    path('password_reset/<uidb64>/<token>/', PasswordReset.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', SetNewPassword.as_view(), name='password_reset_complete'),
]
