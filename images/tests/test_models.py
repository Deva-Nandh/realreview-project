# realreview_backend/images/tests/test_models.py

from django.test import TestCase
from images.models import Image  # Adjust based on your actual model location
from django.contrib.auth.models import User  # Adjust if you're using a custom user model
from datetime import datetime
from django.core.files.uploadedfile import SimpleUploadedFile

class ImageModelTest(TestCase):

    def setUp(self):
        """Create test user and image object"""
        self.user = User.objects.create_user(username='testuser', password='password')
        self.image_data = {
            'image': 'test_image.jpg',  # You can set a mock path or a test file here
            'title': 'Test Image',
            'description': 'A test image description',
            'uploaded_at': datetime.now(),
            'user': self.user,  # If there's a user associated with the image
        }

    def test_image_creation(self):
        """Test image is created successfully"""
        image = Image.objects.create(**self.image_data)
        self.assertEqual(image.title, 'Test Image')
        self.assertEqual(image.user, self.user)  # Assuming there's a foreign key relation

    def test_uploaded_by_field_null(self):
        """Test that 'uploaded_by' can be set to NULL correctly."""
        image = Image.objects.create(image='test_image.jpg', title='Test Image', uploaded_at=datetime.now())
        self.assertIsNone(image.uploaded_by)  # Expecting the 'uploaded_by' field to be NULL

    def test_uploaded_by_invalid_user(self):
        """Test that an invalid user is rejected."""
        # In case you set constraints (if applicable) on 'uploaded_by'
        invalid_data = {
            'image': 'test_image.jpg',
            'title': 'Test Image',
            'description': 'Invalid user test',
            'uploaded_by': 'Testuser1',  # Invalid user format
        }
        with self.assertRaises(ValueError):
            Image.objects.create(**invalid_data)

class ImageUploadTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_image_upload(self):
        """Test image file upload"""
        file = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        image = Image.objects.create(
            image=file,
            title='Test Image',
            description='Test description',
            uploaded_at=datetime.now(),
            user=self.user,
        )
        self.assertEqual(image.image.name, "test_image.jpg")
        self.assertTrue(image.image.storage.exists(image.image.name))  # Verifying file storage
