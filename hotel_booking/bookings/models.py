import uuid

from django.conf import settings
from django.db import models

from hotels.models import HotelRoom


class Booking(models.Model):
    """
    Stores hotel room bookings.
    """

    class BookingStatus(models.TextChoices):
        PENDING = "PENDING", "Pending"
        CONFIRMED = "CONFIRMED", "Confirmed"
        CANCELLED = "CANCELLED", "Cancelled"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    room = models.ForeignKey(
        HotelRoom,
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    check_in_date = models.DateField()

    check_out_date = models.DateField()

    guests = models.PositiveIntegerField(
        default=1,
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    status = models.CharField(
        max_length=20,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "-created_at",
        ]

    def __str__(self):

        return (
            f"{self.user.email} - "
            f"{self.room.title}"
        )