from django.contrib.auth import authenticate
from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True,
        min_length=8,
    )

    class Meta:
        model = User

        fields = (
            "id",
            "email",
            "name",
            "password",
            "role",
        )

        read_only_fields = (
            "id",
        )

    def create(self, validated_data):

        return User.objects.create_user(
            email=validated_data["email"],
            name=validated_data["name"],
            password=validated_data["password"],
            role=validated_data["role"],
        )


class LoginSerializer(serializers.Serializer):
     
    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True,
    )

    def validate(self, attrs):

        user = authenticate(
            email=attrs["email"],
            password=attrs["password"],
        )

        if not user:

            raise serializers.ValidationError(
                "Invalid email or password."
            )

        attrs["user"] = user

        return attrs


class UserSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = User

        fields = (
            "id",
            "email",
            "name",
            "role",
            "date_joined",
        )

    read_only_fields = (
          "id",
          "date_joined",
      )


class UserUpdateSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = User

        fields = (
            "name",
        )


class AdminUserUpdateSerializer(serializers.ModelSerializer):
     
    class Meta:
        model = User

        fields = (
            "name",
            "role",
            "is_active",
        )