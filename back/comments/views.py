from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from comments.services.comments_service import register_comment, get_liked_counts, get_comment_counts, get_comments_list


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comments_registration(request):
    return register_comment(request)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def liked_count(request):
    return get_liked_counts(request)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comments_count(request):
    return get_comment_counts(request)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_comments(request):
    return get_comments_list(request)