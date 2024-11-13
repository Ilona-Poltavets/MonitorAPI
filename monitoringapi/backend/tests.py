from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from .models import Device


class DeviceTests(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test client
        self.client = APIClient()

    def test_create_device(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpassword')

        # Data to create a new device
        data = {
            'device_name': 'Gaming PC',
            'cpu': 'Intel i9',
            'gpu': 'NVIDIA RTX 3080',
            'ram': '32GB',
        }

        # Send POST request to create the device
        response = self.client.post(reverse('device-create'), data, format='json')

        # Verify that the device was created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify that the device was saved to the database
        self.assertEqual(Device.objects.count(), 1)
        self.assertEqual(Device.objects.get().device_name, 'Gaming PC')

    def test_retrieve_devices(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpassword')

        # Create a device for the user
        Device.objects.create(
            user=self.user,
            device_name='Office PC',
            cpu='AMD Ryzen 7',
            gpu='NVIDIA GTX 1660',
            ram='16GB'
        )

        # Send GET request to retrieve all devices
        response = self.client.get(reverse('device-list'), format='json')

        # Verify that the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify that the response contains the created device
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['device_name'], 'Office PC')

    def test_unauthorized_access(self):
        # Attempt to retrieve devices without logging in
        response = self.client.get(reverse('device-list'), format='json')

        # Verify that unauthorized access is forbidden
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
