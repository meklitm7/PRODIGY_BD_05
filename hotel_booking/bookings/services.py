from datetime import timedelta

from django.db.models import Q

from .models import Booking
from hotels.models import HotelRoom


class BookingService:
     
    @staticmethod
    def calculate_total_price(room, check_in, check_out):

        nights = (check_out - check_in).days

        return room.price_per_night * nights

    @staticmethod
    def room_is_available(room, check_in, check_out):

        overlapping_booking = Booking.objects.filter(
            room=room,
            status__in=[
                Booking.BookingStatus.PENDING,
                Booking.BookingStatus.CONFIRMED,
            ],
        ).filter(
            Q(check_in_date__lt=check_out) &
            Q(check_out_date__gt=check_in)
        ).exists()

        return not overlapping_booking

    @staticmethod
    def create_booking(user, validated_data):

        room = validated_data["room"]

        check_in = validated_data["check_in_date"]

        check_out = validated_data["check_out_date"]

        guests = validated_data["guests"]

        if room.owner == user:

            raise ValueError(
                "You cannot book your own room."
            )
        if not room.is_available:

            raise ValueError(
                "This room is currently unavailable."
            )

        if not BookingService.room_is_available(
            room,
            check_in,
            check_out,
        ):

            raise ValueError(
                "Room is not available for these dates."
            )

        total_price = BookingService.calculate_total_price(
            room,
            check_in,
            check_out,
        )

        booking = Booking.objects.create(
            user=user,
            room=room,
            check_in_date=check_in,
            check_out_date=check_out,
            guests=guests,
            total_price=total_price,
        )

        return booking

    @staticmethod
    def get_user_bookings(user):

        return Booking.objects.filter(
            user=user
        )

    @staticmethod
    def get_booking_by_id(booking_id):

        return Booking.objects.get(
            id=booking_id
        )

    @staticmethod
    def cancel_booking(booking):

        booking.status = Booking.BookingStatus.CANCELLED

        booking.save()

        return booking