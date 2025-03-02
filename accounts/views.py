from django.shortcuts import render, get_object_or_404
from .serializers import UserSerializer
from .models import User
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView


class UserListAPIView(APIView):
    def get_permissions(self):
        if self.request.method == "GET":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)

        if request.user.id != user.id:
            return Response(
                {"detail": "자신의 정보만 수정할 수 있습니다."},
                status=status.HTTP_403_FORBIDDEN,
            )

        data = request.data.copy()

        password = data.get("password")
        password2 = data.get("password2")

        print(f"password >>> {repr(password)}, password2 >>>> {repr(password2)}")

        if password:
            if not password2:
                return Response(
                    {"password2": "비밀번호 확인 필드를 입력해야 합니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if password != password2:
                return Response(
                    {"password": "비밀번호가 일치하지 않습니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        data.pop("password2", None)

        serializer = UserSerializer(user, data=data, partial=True)

        if serializer.is_valid():
            user = serializer.save()

            if password:
                user.set_password(password)

                user.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomObtainTokenPairAPIView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = CustomTokenObtainPairSerializer
