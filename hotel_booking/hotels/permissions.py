from rest_framework.permissions import BasePermission


class IsHost(BasePermission):
     
    def has_permission(self, request, view):

        return (
            request.user.is_authenticated
            and request.user.role == "HOST"
        )


class IsRoomOwner(BasePermission):
     
    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):

        return obj.owner == request.user


class IsHostOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        if request.method in ("GET", "HEAD", "OPTIONS"):

            return request.user.is_authenticated

        return (
            request.user.is_authenticated
            and request.user.role == "HOST"
        )