from rest_framework import status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.decorators import (
    api_view,
    permission_classes,
)
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
from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
)


class RegisterView(APIView):

    permission_classes = [AllowAny]

    @extend_schema(
    summary="Register User",
    description=(
        "Create a new user account.\n\n"
        "Roles:\n"
        "- HOST: Can create and manage hotel rooms.\n"
        "- CUSTOMER: Can search and book hotel rooms."
    ),
    request=RegisterSerializer,
    responses=UserSerializer,
    examples=[
        OpenApiExample(
            "Register Example",
            value={
                "email": "customer@example.com",
                "name": "Jane Smith",
                "password": "Password123!"
            },
            request_only=True,
        ),
    ]
    )
     
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

    permission_classes = [AllowAny]

    @extend_schema(
    summary="Login User",
    description=(
        "Authenticate a user using email and password.\n\n"
        "Returns JWT access and refresh tokens upon successful login."
    ),
    request=LoginSerializer,
    examples=[
        OpenApiExample(
            "Login Example",
            value={
                "email": "host@example.com",
                "password": "Password123!"
            },
            request_only=True,
        ),
    ],
)

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
User = get_user_model()


@api_view(["POST"])
@permission_classes([AllowAny])
def create_admin(request):

    if User.objects.filter(is_superuser=True).exists():
        return Response(
            {"error": "Admin already exists."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = User.objects.create_superuser(
        email=request.data["email"],
        password=request.data["password"],
        name=request.data["name"],
    )

    return Response(
        {
            "message": "Admin created successfully.",
            "email": user.email,
        },
        status=status.HTTP_201_CREATED,
    )