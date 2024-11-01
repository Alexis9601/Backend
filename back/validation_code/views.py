from rest_framework.decorators import api_view

from validation_code.services.otpServices import create_otp, otp_validation


@api_view(['POST'])
def generate_otp(request):
    return create_otp(request.data.get('user_id'))

@api_view(['POST'])
def validate_otp(request):
    return otp_validation(request.data.get('user_id'), request.data.get('otp'))