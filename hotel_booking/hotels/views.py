from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import HotelRoom
from .serializers import (
    HotelRoomSerializer,
    HotelRoomCreateUpdateSerializer,
)
from .services import HotelRoomService
from .filters import HotelRoomFilter


class HotelRoomViewSet(viewsets.ModelViewSet):
    """
    Hotel Room CRUD API
    """

    permission_classes = [IsAuthenticated]

    queryset = HotelRoom.objects.all()

    lookup_field = "id"

    filter_backends = [
    DjangoFilterBackend,
    SearchFilter,
    OrderingFilter,
    ]

    filterset_class = HotelRoomFilter

    search_fields = [
        "location",
    ]

    ordering_fields = [
        "price_per_night",
        "created_at",
    ]

    ordering = [
        "-created_at",
    ]

    def get_serializer_class(self):

        if self.action in [
            "create",
            "update",
            "partial_update",
        ]:

            return HotelRoomCreateUpdateSerializer

        return HotelRoomSerializer

    def list(self, request):

      rooms = HotelRoomService.get_all_rooms()

      page = self.paginate_queryset(rooms)

      if page is not None:

          serializer = HotelRoomSerializer(
              page,
              many=True,
          )

          return self.get_paginated_response(
              serializer.data
          )

      serializer = HotelRoomSerializer(
          rooms,
          many=True,
      )

      return Response(serializer.data)
    
    def retrieve(self, request, id=None):

        room = HotelRoomService.get_room_by_id(id)

        serializer = HotelRoomSerializer(room)

        return Response(serializer.data)

    def create(self, request):

        if request.user.role != "HOST":

            return Response(
                {
                    "error": "Only hosts can create hotel rooms."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = HotelRoomCreateUpdateSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        room = HotelRoomService.create_room(
            request.user,
            serializer.validated_data,
        )

        return Response(
            HotelRoomSerializer(room).data,
            status=status.HTTP_201_CREATED,
        )

    def partial_update(self, request, id=None):

        room = HotelRoomService.get_room_by_id(id)

        if room.owner != request.user:

            return Response(
                {
                    "error": "You can only update your own room."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = HotelRoomCreateUpdateSerializer(
            room,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save()

        return Response(
            HotelRoomSerializer(room).data
        )

    def destroy(self, request, id=None):

        room = HotelRoomService.get_room_by_id(id)

        if room.owner != request.user:

            return Response(
                {
                    "error": "You can only delete your own room."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        room.delete()

        return Response(
            {
                "message": "Room deleted successfully."
            },
            status=status.HTTP_200_OK,
        )