from rest_framework.permissions import BasePermission


class IsHost(BasePermission):
    """
    Only hosts can create hotel rooms.
    """

    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.role == "HOST"
        )


class IsRoomOwner(BasePermission):
    """
    Only the room owner can edit or delete it.
    """

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):

        return obj.owner == request.user


class IsHostOrReadOnly(BasePermission):
    """
    Anyone authenticated can view rooms.
    Only hosts can create rooms.
    """

    def has_permission(self, request, view):

        if request.method in ("GET", "HEAD", "OPTIONS"):

            return request.user.is_authenticated

        return (
            request.user.is_authenticated
            and request.user.role == "HOST"
        )