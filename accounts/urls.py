from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = "accounts"
urlpatterns = [
    path("", views.UserListAPIView.as_view(), name="user_list"),
    path("<int:pk>/", views.UserDetailAPIView.as_view(), name="user_detail"),
    path("login/", views.CustomObtainTokenPairAPIView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
