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
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiExample,
)

@extend_schema_view(
    list=extend_schema(
        summary="List My Bookings",
        description=(
            "Retrieve all bookings belonging to the authenticated user."
        ),
        responses=BookingSerializer(many=True),
    ),

    retrieve=extend_schema(
        summary="Retrieve Booking",
        description="Retrieve the details of a booking by its ID.",
        responses=BookingSerializer,
    ),

    create=extend_schema(
        summary="Create Booking",
        description=(
            "Create a booking for a hotel room.\n\n"
            "The total price is calculated automatically based on the "
            "room price and the number of nights."
        ),
        request=BookingCreateSerializer,
        responses=BookingSerializer,
        examples=[
            OpenApiExample(
                "Create Booking",
                value={
                    "room": "2152e4e6-c519-4389-b7cb-6ff8ace923c3",
                    "check_in_date": "2026-07-20",
                    "check_out_date": "2026-07-23",
                    "guests": 2
                },
                request_only=True,
            ),
        ],
    ),

    partial_update=extend_schema(
        summary="Update Booking",
        description=(
            "Update your booking before it is completed or cancelled."
        ),
        request=BookingCreateSerializer,
        responses=BookingSerializer,
    ),

    destroy=extend_schema(
        summary="Cancel Booking",
        description=(
            "Cancel one of your bookings.\n\n"
            "The booking status is changed to **CANCELLED**."
        ),
        responses=BookingSerializer,
    ),
)

class BookingViewSet(viewsets.ModelViewSet):

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

            if request.user.role != "CUSTOMER":
                return Response(
                    {
                        "error": "Only customers can create bookings."
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

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
    
    