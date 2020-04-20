"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path
from rest_framework import routers
from rest_framework_jwt.views import refresh_jwt_token, verify_jwt_token

from blog.api import views


router = routers.DefaultRouter()
router.register(r"api/users", views.UserViewSet)
router.register(r"api/posts", views.PostViewSet)

urlpatterns = [
    path('api/auth', views.CustomObtainJSONWebToken.as_view()),
    path('api/auth/refresh/', refresh_jwt_token),
    path('api/auth/verify/', verify_jwt_token),
    path('api/users/activity/<int:user_id>/',
         views.UserActivityView.as_view()),
    path('api/posts/analytics/', views.MarksAnalyticsView.as_view()),
    path('api/posts/dislike/<int:post_id>/', views.PostDislikeView.as_view()),
    path('api/posts/like/<int:post_id>/', views.PostLikeView.as_view()),
]

urlpatterns += [
    path('', include(router.urls)),
]
