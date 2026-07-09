import django_filters

from .models import HotelRoom


class HotelRoomFilter(django_filters.FilterSet):

    min_price = django_filters.NumberFilter(
        field_name="price_per_night",
        lookup_expr="gte",
    )

    max_price = django_filters.NumberFilter(
        field_name="price_per_night",
        lookup_expr="lte",
    )

    class Meta:

        model = HotelRoom

        fields = [
            "room_type",
            "is_available",
        ]