from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from hotels.models import HotelRoom

class HotelRoomTests(APITestCase):

    def setUp(self):

        self.host = User.objects.create_user(
            email="host@example.com",
            name="Host User",
            password="Password123!",
            role="HOST",
        )

        self.customer = User.objects.create_user(
            email="customer@example.com",
            name="Customer User",
            password="Password123!",
            role="CUSTOMER",
        )

    def test_host_can_create_room(self):

        self.client.force_authenticate(
            user=self.host,
        )

        url = reverse("rooms-list")

        data = {
            "title": "Luxury Suite",
            "description": "Beautiful room",
            "location": "Addis Ababa",
            "price_per_night": "2500.00",
            "capacity": 2,
            "room_type": "SUITE",
            "is_available": True,
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
            HotelRoom.objects.count(),
            1,
        )

        self.assertEqual(
            HotelRoom.objects.first().owner,
            self.host,
        )

    def test_customer_cannot_create_room(self):
        
        #Customers should not be allowed to create hotel rooms.
        
        self.client.force_authenticate(
            user=self.customer,
        )

        url = reverse("rooms-list")

        data = {
            "title": "Luxury Suite",
            "description": "Beautiful room",
            "location": "Addis Ababa",
            "price_per_night": "2500.00",
            "capacity": 2,
            "room_type": "SUITE",
            "is_available": True,
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

        self.assertEqual(
            HotelRoom.objects.count(),
            0,
        )

    def test_list_rooms(self):
        
        #Anyone should be able to view the list of rooms.
        
        HotelRoom.objects.create(
            owner=self.host,
            title="Luxury Suite",
            description="Beautiful room",
            location="Addis Ababa",
            price_per_night="2500.00",
            capacity=2,
            room_type="SUITE",
            is_available=True,
        )

        url = reverse("rooms-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["count"],
            1,
        )

    def test_retrieve_room(self):
         
        room = HotelRoom.objects.create(
            owner=self.host,
            title="Luxury Suite",
            description="Beautiful room",
            location="Addis Ababa",
            price_per_night="2500.00",
            capacity=2,
            room_type="SUITE",
            is_available=True,
        )

        url = reverse(
            "rooms-detail",
            kwargs={"id": room.id},
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["title"],
            "Luxury Suite",
        )

    def test_host_can_update_own_room(self):
            
            #Hosts should be able to update their own rooms.
            
            room = HotelRoom.objects.create(
                owner=self.host,
                title="Luxury Suite",
                description="Beautiful room",
                location="Addis Ababa",
                price_per_night="2500.00",
                capacity=2,
                room_type="SUITE",
                is_available=True,
            )

            self.client.force_authenticate(
                user=self.host,
            )

            url = reverse(
                "rooms-detail",
                kwargs={"id": room.id},
            )

            data = {
                "price_per_night": "3000.00",
            }

            response = self.client.patch(
                url,
                data,
                format="json",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_200_OK,
            )

            room.refresh_from_db()

            self.assertEqual(
                str(room.price_per_night),
                "3000.00",
            )

    def test_host_cannot_update_another_hosts_room(self):
            """
            Hosts should not be able to update rooms
            owned by another host.
            """

            another_host = User.objects.create_user(
                email="host2@example.com",
                name="Host Two",
                password="Password123!",
                role="HOST",
            )

            room = HotelRoom.objects.create(
                owner=another_host,
                title="Luxury Suite",
                description="Beautiful room",
                location="Addis Ababa",
                price_per_night="2500.00",
                capacity=2,
                room_type="SUITE",
                is_available=True,
            )

            self.client.force_authenticate(
                user=self.host,
            )

            url = reverse(
                "rooms-detail",
                kwargs={"id": room.id},
            )

            response = self.client.patch(
                url,
                {
                    "price_per_night": "5000.00",
                },
                format="json",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_403_FORBIDDEN,
            )

    def test_host_can_delete_own_room(self):
            
            #Hosts should be able to delete their own rooms.
            
            room = HotelRoom.objects.create(
                owner=self.host,
                title="Luxury Suite",
                description="Beautiful room",
                location="Addis Ababa",
                price_per_night="2500.00",
                capacity=2,
                room_type="SUITE",
                is_available=True,
            )

            self.client.force_authenticate(
                user=self.host,
            )

            url = reverse(
                "rooms-detail",
                kwargs={"id": room.id},
            )

            response = self.client.delete(url)

            self.assertEqual(
                response.status_code,
                status.HTTP_200_OK,
            )

            self.assertEqual(
                HotelRoom.objects.count(),
                0,
            )

    def test_host_cannot_delete_another_hosts_room(self):
            """
            Hosts should not be able to delete rooms
            owned by another host.
            """

            another_host = User.objects.create_user(
                email="host2@example.com",
                name="Host Two",
                password="Password123!",
                role="HOST",
            )

            room = HotelRoom.objects.create(
                owner=another_host,
                title="Luxury Suite",
                description="Beautiful room",
                location="Addis Ababa",
                price_per_night="2500.00",
                capacity=2,
                room_type="SUITE",
                is_available=True,
            )

            self.client.force_authenticate(
                user=self.host,
            )

            url = reverse(
                "rooms-detail",
                kwargs={"id": room.id},
            )

            response = self.client.delete(url)

            self.assertEqual(
                response.status_code,
                status.HTTP_403_FORBIDDEN,
            )

            self.assertEqual(
                HotelRoom.objects.count(),
                1,
            )