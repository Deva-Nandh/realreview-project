from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Image, Rating
from django.urls import reverse
from io import BytesIO
from PIL import Image as PilImage


class ImageUploadTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def generate_test_image(self):
        file = BytesIO()
        image = PilImage.new('RGB', (100, 100), 'blue')
        image.save(file, 'JPEG')
        file.name = 'test.jpg'
        file.seek(0)
        return file

    def test_upload_image(self):
        url = reverse('image-upload')
        data = {
            'image': self.generate_test_image(),
            'location': 'Test Location',
        }
        response = self.client.post(url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Image.objects.count(), 1)


class RatingCreateTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='rater', password='testpass')
        self.image = Image.objects.create(
            image='images/test.jpg',
            user=self.user,
            location='Location 1'
        )
        self.client.login(username='rater', password='testpass')

    def test_create_rating(self):
        url = reverse('image-rate', kwargs={'pk': self.image.pk})
        data = {'rating': 4}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Rating.objects.count(), 1)
