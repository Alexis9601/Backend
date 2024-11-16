from rest_framework.decorators import api_view

from validation_code.services.otpServices import create_otp, otp_validation, create_recover_otp, otp_recover_validation


@api_view(['POST'])
def generate_otp(request):
    return create_otp(request.data.get('user_id'))

@api_view(['POST'])
def validate_otp(request):
    return otp_validation(request.data.get('user_id'), request.data.get('otp'))

@api_view(['POST'])
def generate_recover_otp(request):
    return create_recover_otp(request.data.get('email'))

@api_view(['POST'])
def validate_recover_otp(request):
    return otp_recover_validation(request.data.get('email'), request.data.get('otp'))
