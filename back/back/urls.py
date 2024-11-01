from django.urls import path

from user.views import user_registration, login_user
from validation_code.views import generate_otp, validate_otp

urlpatterns = [
    path('user/register', user_registration, name='user-registration'),
    path('user/login', login_user, name='login-user'),
    path('validation/otp', generate_otp, name='generate-otp'),
    path('validation/validateOtp', validate_otp, name='validate-otp'),
]
