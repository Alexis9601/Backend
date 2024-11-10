from django.urls import path

from itinerary.views import get_today_itineraries
from user.views import user_registration, login_user, user_basic_info, update
from validation_code.views import generate_otp, validate_otp

urlpatterns = [
    path('user/register', user_registration, name='user-registration'),
    path('user/login', login_user, name='login-user'),
    path('user/info', user_basic_info, name='user-basic-info'),
    path('user/update', update, name='user-update'),
    path('validation/otp', generate_otp, name='generate-otp'),
    path('validation/validateOtp', validate_otp, name='validate-otp'),
    path('itinerary/todayItineraries', get_today_itineraries, name='today-itineraries'),
]
