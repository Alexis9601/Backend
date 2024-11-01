from django.urls import path

from db.views import user_registration, generate_otp

urlpatterns = [
    path('user/register/', user_registration, name='user-registration'),
    path('user/otp/', generate_otp, name='generate-otp'),
]
