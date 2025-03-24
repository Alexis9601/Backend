from django.urls import path

from comments.views import comments_registration, liked_count, comments_count, get_comments
from itinerary.views import get_today_itineraries, generate_itineraries, save_itinerary, get_day, get_user_itineraries, \
    delete_itinerary
from user.views import user_registration, login_user, user_basic_info, update, update_user_password
from validation_code.views import generate_otp, validate_otp, generate_recover_otp, validate_recover_otp

urlpatterns = [
    path('user/register', user_registration, name='user-registration'),
    path('user/login', login_user, name='login-user'),
    path('user/info', user_basic_info, name='user-basic-info'),
    path('user/update', update, name='user-update'),
    path('user/updatePassword', update_user_password, name='user-update-password'),
    path('validation/otp', generate_otp, name='generate-otp'),
    path('validation/recoverOtp', generate_recover_otp, name='generate-recover-otp'),
    path('validation/validateOtp', validate_otp, name='validate-otp'),
    path('validation/validateRecoverOtp', validate_recover_otp, name='validate-recover-otp'),
    path('itinerary/todayItineraries', get_today_itineraries, name='today-itineraries'),
    path('itinerary/generateItineraries', generate_itineraries, name='generate-itineraries'),
    path('itinerary/save', save_itinerary, name='save-itinerary'),
    path('itinerary/getByDay/<uuid:id>', get_day, name='get-day'),
    path('itinerary/itineraries', get_user_itineraries, name='get-user-itineraries'),
    path('itinerary/<uuid:id>', delete_itinerary, name='delete-itinerary'),
    path('comments/register', comments_registration, name='comments-registration'),
    path('comments/likedCount', liked_count, name='licked-count'),
    path('comments/commentsCount', comments_count, name='comments-count'),
    path('comments/getComments', get_comments, name='get-comments')
]
