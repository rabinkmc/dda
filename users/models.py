from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    @property
    def is_student(self):
        return hasattr(self, "student")

    @property
    def is_instructor(self):
        return hasattr(self, "instructor")

    @property
    def is_admin(self):
        return self.is_staff
