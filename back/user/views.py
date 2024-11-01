from rest_framework.decorators import api_view
from user.services.user_services import register_user, login


@api_view(['POST'])
def user_registration(request):
    return register_user(request)

@api_view(['POST'])
def login_user(request):
    return login(request)