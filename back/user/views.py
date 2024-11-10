from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from user.services.user_services import register_user, login, basic_info, update_user


@api_view(['POST'])
def user_registration(request):
    return register_user(request)

@api_view(['POST'])
def login_user(request):
    return login(request)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_basic_info(request):
    return basic_info(request.user)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update(request):
    return update_user(request.user, request.data)