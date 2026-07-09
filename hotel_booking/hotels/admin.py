from django.contrib import admin

from .models import HotelRoom


@admin.register(HotelRoom)
class HotelRoomAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "owner",
        "location",
        "price_per_night",
        "room_type",
        "is_available",
    )

    search_fields = (
        "title",
        "location",
    )

    list_filter = (
        "room_type",
        "is_available",
    )