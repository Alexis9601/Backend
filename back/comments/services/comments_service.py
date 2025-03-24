from datetime import datetime

from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from comments.models import Comments

def register_comment(request):
    try:
        data = request.data

        if 'liked' not in data:
            return Response({"success": False, "error": "Faltan campos obligatorios"}, status=200)

        Comments.objects.create(
            liked=data['liked'],
            comments=data.get('comments', ''),
            user_id=request.user
        )

        return Response({
            "success": True,
            "error": None
        }, status=201)

    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=500)

def get_liked_counts(request):
    try:
        data = request.data
        start_date = data.get("startDate", None)
        end_date = data.get("endDate", None)

        filters = {}
        if start_date:
            filters["created_at__gte"] = datetime.strptime(start_date, "%Y-%m-%d").replace(hour=0, minute=0, second=0)

        if end_date:
            filters["created_at__lte"] = datetime.strptime(end_date, "%Y-%m-%d").replace(hour=23, minute=59, second=59)

        comments = Comments.objects.filter(**filters)

        liked_true_count = comments.filter(liked=True).count()
        liked_false_count = comments.filter(liked=False).count()

        data = {
            "trueCount": liked_true_count,
            "falseCount": liked_false_count
        }

        return Response({
            "success": True,
            "error": None,
            "data": data
        }, status=200)

    except Exception as e:
        return Response({"success": False, "error": str(e), "data": None }, status=500)

def get_comment_counts(request):
    try:
        data = request.data
        start_date = data.get("startDate", None)
        end_date = data.get("endDate", None)

        filters = {"comments__isnull": False, "comments__gt": ""}

        if start_date:
            filters["created_at__gte"] = datetime.strptime(start_date, "%Y-%m-%d").replace(hour=0, minute=0, second=0)

        if end_date:
            filters["created_at__lte"] = datetime.strptime(end_date, "%Y-%m-%d").replace(hour=23, minute=59, second=59)

        comment_count = Comments.objects.filter(**filters).count()

        return Response({
            "success": True,
            "commentCount": comment_count,
            "error": None
        }, status=200)

    except Exception as e:
        return Response({"success": False, "error": str(e), "commentCount": None}, status=500)

def get_comments_list(request):
    try:
        data = request.data
        start_date = data.get("start_date", None)
        end_date = data.get("end_date", None)
        page = int(data.get("page", 1))
        size = int(data.get("size", 10))

        filters = {
            "comments__isnull": False,
            "comments__gt": ""
        }

        if start_date:
            filters["created_at__gte"] = datetime.strptime(start_date, "%Y-%m-%d").replace(hour=0, minute=0, second=0)

        if end_date:
            filters["created_at__lte"] = datetime.strptime(end_date, "%Y-%m-%d").replace(hour=23, minute=59, second=59)

        comments = Comments.objects.filter(**filters).select_related("user_id").order_by("-created_at")

        paginator = Paginator(comments, size)
        total_pages = paginator.num_pages

        try:
            comments_page = paginator.page(page)
        except:
            return Response({"success": False, "error": "Página fuera de rango"}, status=400)

        comment_list = [{
            "id": comment.id,
            "comment": comment.comments,
            "liked": comment.liked,
            "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "user": {
                "name": f"{comment.user_id.user_name} {comment.user_id.user_lastname}",
                "email": comment.user_id.email
            }
        } for comment in comments_page]

        return Response({
            "success": True,
            "comments": comment_list,
            "total_pages": total_pages,
            "is_last_page": page >= total_pages,
            "error": None
        })

    except Exception as e:
        return Response({"success": False, "error": str(e), "comments": None}, status=500)