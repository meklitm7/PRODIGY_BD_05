from django.db.models import Q

from hotels.models import HotelRoom
from bookings.models import Booking

from .parsers import QueryParser


class AISearchService:

    @staticmethod
    def filter_available_rooms(rooms, check_in, check_out):
         
        unavailable_rooms = Booking.objects.filter(
            status__in=[
                Booking.BookingStatus.PENDING,
                Booking.BookingStatus.CONFIRMED,
            ]
        ).filter(
            check_in_date__lt=check_out,
            check_out_date__gt=check_in,
        ).values_list(
            "room_id",
            flat=True,
        )

        return rooms.exclude(
            id__in=unavailable_rooms
        )

    @staticmethod
    def search(query):
         
        filters = QueryParser.parse(query)

        rooms = HotelRoom.objects.all()

         
        if "location" in filters:
            rooms = rooms.filter(
                location__icontains=filters["location"]
            )

         
        if "room_type" in filters:
            rooms = rooms.filter(
                room_type=filters["room_type"]
            )

         
        if "guests" in filters:
            rooms = rooms.filter(
                capacity__gte=filters["guests"]
            )

         
        if "price" in filters:
            if filters["price"] == "cheap":
                rooms = rooms.order_by(
                    "price_per_night"
                )
            else:
                rooms = rooms.order_by(
                    "-price_per_night"
                )

         
        if (
            "check_in" in filters and
            "check_out" in filters
        ):
            rooms = AISearchService.filter_available_rooms(
                rooms,
                filters["check_in"],
                filters["check_out"],
            )

        return rooms