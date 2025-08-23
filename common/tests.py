from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseTestCase(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            first_name="admin",
            last_name="admin",
            username="admin",
            email="admin@email.com",
            password="admin123",
        )
        self.user = User.objects.create_user(
            first_name="john",
            last_name="doe",
            username="john",
            email="john@email.com",
            password="john123",
        )
