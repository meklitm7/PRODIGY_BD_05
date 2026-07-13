from datetime import date, timedelta

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone
from users.models import User
from hotels.models import HotelRoom
from bookings.models import Booking

class BookingTests(APITestCase):

    def setUp(self):

        self.host = User.objects.create_user(
            email="host@example.com",
            name="Host",
            password="Password123!",
            role="HOST",
        )

        self.customer = User.objects.create_user(
            email="customer@example.com",
            name="Customer",
            password="Password123!",
            role="CUSTOMER",
        )

        self.room = HotelRoom.objects.create(
            owner=self.host,
            title="Luxury Suite",
            description="Beautiful room",
            location="Addis Ababa",
            price_per_night="2500.00",
            capacity=2,
            room_type="SUITE",
            is_available=True,
        )

    def test_customer_can_create_booking(self):
        
        #Customers should be able to create bookings.
         
        self.client.force_authenticate(
            user=self.customer,
        )

        url = reverse("booking-list")

        data = {
            "room": str(self.room.id),
            "check_in_date": str(
                date.today() + timedelta(days=1)
            ),
            "check_out_date": str(
                date.today() + timedelta(days=3)
            ),
            "guests": 2,
        }

        response = self.client.post(
            url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            Booking.objects.count(),
            1,
        )

    def test_cannot_double_book_room(self):
        
        #The same room cannot be booked twice for overlapping dates.

        Booking.objects.create(
            user=self.customer,
            room=self.room,
            check_in_date=date.today() + timedelta(days=1),
            check_out_date=date.today() + timedelta(days=3),
            guests=2,
            total_price=5000,
            status=Booking.BookingStatus.CONFIRMED,
        )

        second_customer = User.objects.create_user(
            email="customer2@example.com",
            name="Customer Two",
            password="Password123!",
            role="CUSTOMER",
        )

        self.client.force_authenticate(user=second_customer)

        url = reverse("booking-list")

        data = {
            "room": str(self.room.id),
            "check_in_date": str(date.today() + timedelta(days=2)),
            "check_out_date": str(date.today() + timedelta(days=4)),
            "guests": 2,
        }

        response = self.client.post(
            url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_host_cannot_create_booking(self):
        
        #Hosts should not be allowed to create bookings.
        
        self.client.force_authenticate(
            user=self.host,
        )

        url = reverse("booking-list")

        data = {
            "room": str(self.room.id),
            "check_in_date": str(date.today() + timedelta(days=1)),
            "check_out_date": str(date.today() + timedelta(days=3)),
            "guests": 2,
        }

        response = self.client.post(
            url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_customer_can_cancel_own_booking(self):
        
        #A customer should be able to cancel their own booking.
    
        booking = Booking.objects.create(
            user=self.customer,
            room=self.room,
            check_in_date=date.today() + timedelta(days=1),
            check_out_date=date.today() + timedelta(days=3),
            guests=2,
            total_price=5000,
            status=Booking.BookingStatus.PENDING,
        )

        self.client.force_authenticate(
            user=self.customer,
        )

        url = reverse(
            "booking-detail",
            kwargs={"id": booking.id},
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        booking.refresh_from_db()

        self.assertEqual(
            booking.status,
            Booking.BookingStatus.CANCELLED,
        )

    def test_customer_cannot_cancel_other_users_booking(self):
        
        #A customer should not be able to cancel another customer's booking.
        
        other_customer = User.objects.create_user(
            email="customer2@example.com",
            name="Customer Two",
            password="Password123!",
            role="CUSTOMER",
        )

        booking = Booking.objects.create(
            user=other_customer,
            room=self.room,
            check_in_date=date.today() + timedelta(days=1),
            check_out_date=date.today() + timedelta(days=3),
            guests=2,
            total_price=5000,
            status=Booking.BookingStatus.PENDING,
        )

        self.client.force_authenticate(
            user=self.customer,
        )

        url = reverse(
            "booking-detail",
            kwargs={"id": booking.id},
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_invalid_booking_dates(self):

            self.client.force_authenticate(
                user=self.customer,
            )

            url = reverse("booking-list")

            today = timezone.now().date()

            response = self.client.post(
                url,
                {
                    "room": str(self.room.id),
                    "check_in_date": today + timedelta(days=5),
                    "check_out_date": today + timedelta(days=4),
                    "guests": 2,
                },
                format="json",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_400_BAD_REQUEST,
            )

    def test_customer_cannot_view_other_users_booking(self):

            another_customer = User.objects.create_user(
                email="customer2@example.com",
                name="Customer Two",
                password="Password123!",
                role="CUSTOMER",
            )

            booking = Booking.objects.create(
                user=another_customer,
                room=self.room,
                check_in_date=date.today() + timedelta(days=1),
                check_out_date=date.today() + timedelta(days=3),
                guests=2,
                total_price=5000,
            )

            self.client.force_authenticate(
                user=self.customer,
            )

            url = reverse(
                "booking-detail",
                kwargs={"id": booking.id},
            )

            response = self.client.get(url)

            self.assertEqual(
                response.status_code,
                status.HTTP_403_FORBIDDEN,
            )