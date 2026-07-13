from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from users.models import User
from hotels.models import HotelRoom


class AISearchTests(APITestCase):

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

        HotelRoom.objects.create(
            owner=self.host,
            title="Luxury Suite",
            description="Ocean View",
            location="Addis Ababa",
            price_per_night=2500,
            capacity=2,
            room_type="SUITE",
            is_available=True,
    )

    def test_ai_search_returns_rooms(self):

        self.client.force_authenticate(
            user=self.customer,
        )

        url = reverse("ai-search")

        response = self.client.post(
            url,
            {
                "query": "suite",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["title"],
            "Luxury Suite",
        )

    def test_ai_search_requires_authentication(self):

        url = reverse("ai-search")

        response = self.client.post(
            url,
            {
                "query": "suite"
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_empty_search_query(self):

        self.client.force_authenticate(
            user=self.customer,
        )

        url = reverse("ai-search")

        response = self.client.post(
            url,
            {
                "query": ""
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_search_returns_no_rooms(self):

        self.client.force_authenticate(
            user=self.customer,
        )

        url = reverse("ai-search")

        response = self.client.post(
            url,
            {
                "query": "Family room",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            0,
        )

    