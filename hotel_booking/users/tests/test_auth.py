from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class AuthenticationTests(APITestCase):

    def test_register_user(self):
        
        #Test that a new customer can register successfully.
        
        url = reverse("register")

        data = {
            "email": "customer@example.com",
            "name": "John Doe",
            "password": "Password123!",
            "role": "CUSTOMER",
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
            User.objects.count(),
            1,
        )

        self.assertEqual(
            User.objects.first().email,
            "customer@example.com",
        )
    def test_login_user(self):
        """
        Test that a registered user can log in
        and receive JWT tokens.
        """

        User.objects.create_user(
            email="customer@example.com",
            name="John Doe",
            password="Password123!",
            role="CUSTOMER",
        )

        url = reverse("login")

        data = {
            "email": "customer@example.com",
            "password": "Password123!",
        }

        response = self.client.post(
            url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn(
            "access",
            response.data,
        )

        self.assertIn(
            "refresh",
            response.data,
        )
    def test_login_invalid_credentials(self):
        
        #Test login with an incorrect password.
        
        User.objects.create_user(
            email="customer@example.com",
            name="John Doe",
            password="Password123!",
            role="CUSTOMER",
        )

        url = reverse("login")

        data = {
            "email": "customer@example.com",
            "password": "WrongPassword",
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