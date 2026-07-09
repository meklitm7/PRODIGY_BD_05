from rest_framework import serializers

from .models import HotelRoom


class HotelRoomSerializer(serializers.ModelSerializer):
    """
    Used for returning hotel room information.
    """

    owner = serializers.ReadOnlyField(source="owner.email")

    class Meta:
        model = HotelRoom

        fields = (
            "id",
            "owner",
            "title",
            "description",
            "location",
            "price_per_night",
            "capacity",
            "room_type",
            "is_available",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "owner",
            "created_at",
            "updated_at",
        )


class HotelRoomCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Used for creating and updating hotel rooms.
    """

    class Meta:
        model = HotelRoom

        fields = (
            "title",
            "description",
            "location",
            "price_per_night",
            "capacity",
            "room_type",
            "is_available",
        )

    def validate_price_per_night(self, value):

        if value <= 0:

            raise serializers.ValidationError(
                "Price must be greater than zero."
            )

        return value

    def validate_capacity(self, value):

        if value <= 0:

            raise serializers.ValidationError(
                "Capacity must be greater than zero."
            )

        return value