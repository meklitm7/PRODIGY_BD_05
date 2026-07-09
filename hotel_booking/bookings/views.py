from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Booking
from .serializers import (
    BookingSerializer,
    BookingCreateSerializer,
)
from .services import BookingService


class BookingViewSet(viewsets.ModelViewSet):
    """
    Booking API.
    """

    permission_classes = [IsAuthenticated]

    queryset = Booking.objects.all()

    lookup_field = "id"

    http_method_names = [
        "get",
        "post",
        "delete",
    ]

    def get_serializer_class(self):

        if self.action == "create":

            return BookingCreateSerializer

        return BookingSerializer

    def list(self, request):

        bookings = BookingService.get_user_bookings(
            request.user
        )

        page = self.paginate_queryset(bookings)

        if page is not None:

            serializer = BookingSerializer(
                page,
                many=True,
            )

            return self.get_paginated_response(
                serializer.data
            )

        serializer = BookingSerializer(
            bookings,
            many=True,
        )

        return Response(serializer.data)

    def retrieve(self, request, id=None):

        booking = BookingService.get_booking_by_id(id)

        if booking.user != request.user:

            return Response(
                {
                    "error": "You do not have permission to view this booking."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = BookingSerializer(
            booking
        )

        return Response(serializer.data)

    def create(self, request):

        serializer = BookingCreateSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        try:

            booking = BookingService.create_booking(
                request.user,
                serializer.validated_data,
            )

        except ValueError as error:

            return Response(
                {
                    "error": str(error)
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            BookingSerializer(
                booking
            ).data,
            status=status.HTTP_201_CREATED,
        )

    def destroy(self, request, id=None):

        booking = BookingService.get_booking_by_id(id)

        if booking.user != request.user:

            return Response(
                {
                    "error": "You can only cancel your own booking."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        BookingService.cancel_booking(
            booking
        )

        return Response(
            {
                "message": "Booking cancelled successfully."
            },
            status=status.HTTP_200_OK,
        )