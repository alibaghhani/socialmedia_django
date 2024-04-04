from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model


class SigninViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(username='testuser', password='password123',phone_number='09126532514')

    def test_login_view(self):
        # Define the login data
        login_data = {
            'username': 'testuser',
            'password': 'password123',
            'phone_number': '09126532514'
        }

        # Post the login data to the SigninView
        response = self.client.post(reverse('login'), login_data)

        # Check if the response status code is 200
        self.assertEqual(response.status_code, 200)

        # Optionally, you can check if the user is redirected to the home page after successful login
        self.assertRedirects(response, reverse('home'))

        # Optionally, you can check if the user is logged in
        self.assertTrue(response.wsgi_request.user.is_authenticated)
