from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsAdmin
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    UserUpdateSerializer,
    AdminUserUpdateSerializer,
)
from .services import UserService


class RegisterView(APIView):
     
    def post(self, request):

        serializer = RegisterSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        user = UserService.register_user(
            serializer.validated_data,
        )

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):

    def post(self, request):

        serializer = LoginSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            },
            status=status.HTTP_200_OK,
        )


class ProfileView(APIView):
     
    permission_classes = [IsAuthenticated]

    def get(self, request):

        serializer = UserSerializer(
            request.user,
        )

        return Response(serializer.data)

    def patch(self, request):

        serializer = UserUpdateSerializer(
            request.user,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        UserService.update_user(
            request.user,
            serializer.validated_data,
        )

        return Response(
            UserSerializer(request.user).data
        )


class UserListView(APIView):
     
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):

        users = UserService.get_all_users()

        serializer = UserSerializer(
            users,
            many=True,
        )

        return Response(serializer.data)


class UserDetailView(APIView):
     
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, id):

        try:

            user = UserService.get_user_by_id(id)

        except User.DoesNotExist:

            return Response(
                {
                    "error": "User not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = UserSerializer(user)

        return Response(serializer.data)

    def patch(self, request, id):

        try:

            user = UserService.get_user_by_id(id)

        except User.DoesNotExist:

            return Response(
                {
                    "error": "User not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = AdminUserUpdateSerializer(
            user,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        UserService.update_user(
            user,
            serializer.validated_data,
        )

        return Response(
            UserSerializer(user).data
        )

    def delete(self, request, id):

        try:

            user = UserService.get_user_by_id(id)

        except User.DoesNotExist:

            return Response(
                {
                    "error": "User not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        UserService.delete_user(user)

        return Response(
            {
                "message": "User deleted successfully."
            },
            status=status.HTTP_200_OK,
        )