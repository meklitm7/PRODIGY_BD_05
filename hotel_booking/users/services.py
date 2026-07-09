from .models import User


class UserService:
    """
    Business logic for users.
    """

    @staticmethod
    def register_user(validated_data):
        """
        Register a new user.
        """

        return User.objects.create_user(
            email=validated_data["email"],
            name=validated_data["name"],
            password=validated_data["password"],
            role=validated_data["role"],
        )

    @staticmethod
    def get_all_users():
        """
        Return all users.
        """

        return User.objects.all()

    @staticmethod
    def get_user_by_id(user_id):
        """
        Return a user by UUID.
        """

        return User.objects.get(id=user_id)

    @staticmethod
    def update_user(user, validated_data):
        """
        Update user information.
        """

        for field, value in validated_data.items():

            setattr(user, field, value)

        user.save()

        return user

    @staticmethod
    def delete_user(user):
        """
        Delete a user.
        """

        user.delete()