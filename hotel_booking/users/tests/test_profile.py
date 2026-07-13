from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class ProfileTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="customer@example.com",
            name="John Doe",
            password="Password123!",
            role="CUSTOMER",
        )

    def test_get_profile(self):
        """
        Authenticated users should be able to
        retrieve their profile.
        """

        self.client.force_authenticate(
            user=self.user,
        )

        url = reverse("profile")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["email"],
            self.user.email,
        )

    def test_update_profile(self):
        """
        Authenticated users should be able to update
        their own profile.
        """

        self.client.force_authenticate(
            user=self.user,
        )

        url = reverse("profile")

        data = {
            "name": "Updated Name",
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

        self.user.refresh_from_db()

        self.assertEqual(
            self.user.name,
            "Updated Name",
        )

    def test_profile_requires_authentication(self):
        
        #Anonymous users should not access the profile endpoint.
        
        url = reverse("profile")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )