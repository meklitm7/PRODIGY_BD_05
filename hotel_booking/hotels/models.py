import uuid

from django.db import models
from django.conf import settings


class HotelRoom(models.Model):

    class RoomType(models.TextChoices):

        SINGLE = "SINGLE", "Single"

        DOUBLE = "DOUBLE", "Double"

        SUITE = "SUITE", "Suite"

        FAMILY = "FAMILY", "Family"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="rooms",
    )

    title = models.CharField(
        max_length=255,
    )

    description = models.TextField()

    location = models.CharField(
        max_length=255,
    )

    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    capacity = models.PositiveIntegerField()

    room_type = models.CharField(
        max_length=20,
        choices=RoomType.choices,
    )

    is_available = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):

        return self.title