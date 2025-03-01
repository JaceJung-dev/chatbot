from django.urls import path
from . import views

app_name = "accounts"
urlpatterns = [
    path("", views.UserListAPIView.as_view(), name="user_list"),
    path("<int:pk>/", views.UserDetailAPIView.as_view(), name="user_detail"),
]
