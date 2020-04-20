from datetime import timedelta, date

from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.db.models import Count
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebToken

from blog.api.models import Post, PostMark
from blog.api.serializers import PostSerializer, UserSerializer


class CustomObtainJSONWebToken(ObtainJSONWebToken):
    """Override standard obtaining of JWT token for setting last login
    user's field"""

    def post(self, request, *args, **kwargs):
        """Action for POST method of this view"""

        result = super().post(request, *args, **kwargs)
        try:
            user = get_user_model().objects.get(
                username=request.data['username']
            )
            update_last_login(None, user)
        except get_user_model().DoesNotExist:
            pass

        return result


class MarksAnalyticsView(APIView):
    """View for likes/dislikes analytics in chosen period"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Action for GET method of this view"""

        # Date range parameters
        date_from = request.query_params.get("date_from", date.today())
        date_to = request.query_params.get(
            "date_to",
            date.today() + timedelta(days=1)
        )

        # Getting data and convert in needed format
        data = (PostMark
                .objects
                .filter(datetime__range=[date_from, date_to])
                .values("datetime__date", "sign")
                .annotate(total=Count('id')))

        result = {}

        # Iterate each exists element to setting likes and dislikes count
        for item in data:

            item_date, sign, total = item.values()

            item_date = str(item_date)

            if item_date not in result:
                result[item_date] = {}

            if sign == "True":
                result[item_date]["likes"] = total

            if sign == "False":
                result[item_date]["dislikes"] = total

        return Response(result)


class PostDislikeView(APIView):
    """View for disliking posts"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, post_id):
        """Action for GET method of this view"""

        post = Post.objects.filter(pk=post_id).first()

        if not post:
            return Response({"error": "Post not found"},
                            status=status.HTTP_404_NOT_FOUND)

        if post.dislike_post():
            return Response({"message": "You successfully disliked the post!"})

        return Response({"message": "You successfully undisliked the post!"})


class PostLikeView(APIView):
    """View for liking posts"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, post_id):
        """Action for GET method of this view"""

        post = Post.objects.filter(pk=post_id).first()

        if not post:
            return Response({"error": "Post not found"},
                            status=status.HTTP_404_NOT_FOUND)

        if post.like_post():
            return Response({"message": "You successfully liked the post!"})

        return Response({"message": "You successfully unliked the post!"})


class PostViewSet(viewsets.ModelViewSet):
    """View set for User model"""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserActivityView(APIView):
    """View for user's activity of last login and last action params"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, user_id):
        """Action for GET method of this view"""

        data = (get_user_model()
                .objects
                .filter(pk=user_id)
                .values("last_action", "last_login"))

        if not data:
            return Response({"error": "User not found"},
                            status=status.HTTP_404_NOT_FOUND)

        return Response(data)


class UserViewSet(viewsets.ModelViewSet):
    """View set for User model"""

    queryset = get_user_model().objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
