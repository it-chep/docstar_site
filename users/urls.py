
from django.urls import path, include

from .views import *


urlpatterns = [
    # path('login/', RegistrationAPIView.as_view(), name='login'),
    path('signup/', SignUp.as_view(), name='signup'),
    path('signup/success/', success_signup, name='success'),
    # path('login/', Login.as_view(), name='login'),
    # path('forgot_password/', Forgot_pass.as_view, name='forgot_password'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verificate_email/', VerificationEmail.as_view(), name='verfi_email'),
    path('verificate_email/get_token/', GetToken.as_view(), name='get_token'),
    path('forgot_password/', ForgotPassword.as_view(), name='forgot_password'),
    path('forgot_password/validate_token/', ValidateToken.as_view(), name='validate_token'),
    path('forgot_password/validate_token/error', InvalidToken.as_view(), name='invalid_token'),
    path('forgot_password/validate_token/change_password/', ChangePassword.as_view(), name='change_password'),

    path('', include('django.contrib.auth.urls')),
]

handler404 = "docstar_site.views.page_not_found_view"

