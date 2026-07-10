from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.role == "ADMIN"
        )


class IsHost(BasePermission):
    """
    Allows access only to hosts.
    """

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.role == "HOST"
        )


class IsCustomer(BasePermission):
    """
    Allows access only to customers.
    """

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.role == "CUSTOMER"
        )


class IsAdminOrHost(BasePermission):
     
    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.role in [
                "ADMIN",
                "HOST",
            ]
        )