from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)
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
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiExample,
)

@extend_schema_view(
    list=extend_schema(
        summary="List Hotel Rooms",
        description=(
            "Retrieve a paginated list of hotel rooms.\n\n"
            "Supports filtering, searching, ordering, and Redis caching."
        ),
        responses=HotelRoomSerializer(many=True),
    ),

    retrieve=extend_schema(
        summary="Retrieve Hotel Room",
        description="Retrieve the details of a hotel room using its ID.",
        responses=HotelRoomSerializer,
    ),

    create=extend_schema(
        summary="Create Hotel Room",
        description=(
            "Create a new hotel room.\n\n"
            "Only authenticated users with the **HOST** role "
            "can create hotel rooms."
        ),
        request=HotelRoomCreateUpdateSerializer,
        responses=HotelRoomSerializer,
        examples=[
            OpenApiExample(
                "Create Hotel Room",
                value={
                    "title": "Luxury Suite",
                    "description": "Beautiful suite with city view.",
                    "location": "Addis Ababa",
                    "price_per_night": "2500.00",
                    "capacity": 2,
                    "room_type": "SUITE",
                    "is_available": True
                },
                request_only=True,
            ),
        ],
    ),

    partial_update=extend_schema(
        summary="Update Hotel Room",
        description="Partially update one of your own hotel rooms.",
        request=HotelRoomCreateUpdateSerializer,
        responses=HotelRoomSerializer,
    ),

    destroy=extend_schema(
        summary="Delete Hotel Room",
        description="Delete one of your own hotel rooms.",
        responses={204: None},
    ),
)

class HotelRoomViewSet(viewsets.ModelViewSet):

    def get_permissions(self):

        if self.action in [
            "list",
            "retrieve",
        ]:
            return [AllowAny()]

        return [IsAuthenticated()]

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

        queryset = self.filter_queryset(
            HotelRoom.objects.all()
        )

        rooms = HotelRoomService.search_rooms(
            queryset,
            request.query_params,
        )

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

        room = HotelRoomService.update_room(
            room,
            serializer.validated_data,
        )

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

        HotelRoomService.delete_room(room)

        return Response(
            {
                "message": "Room deleted successfully."
            },
            status=status.HTTP_200_OK,
        )