from datetime import date

from rest_framework import serializers

from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
     

    room_title = serializers.CharField(
        source="room.title",
        read_only=True,
    )

    class Meta:
        model = Booking

        fields = (
            "id",
            "room",
            "room_title",
            "check_in_date",
            "check_out_date",
            "guests",
            "total_price",
            "status",
            "created_at",
        )

        read_only_fields = (
            "id",
            "total_price",
            "status",
            "created_at",
        )


class BookingCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking

        fields = (
            "room",
            "check_in_date",
            "check_out_date",
            "guests",
        )

    def validate(self, attrs):

        check_in = attrs["check_in_date"]
        check_out = attrs["check_out_date"]

        if check_in < date.today():

            raise serializers.ValidationError(
                "Check-in date cannot be in the past."
            )

        if check_out <= check_in:

            raise serializers.ValidationError(
                "Check-out date must be after check-in date."
            )

        if attrs["guests"] <= 0:

            raise serializers.ValidationError(
                "Guests must be greater than zero."
            )

        return attrs