import os
import django
import random

# Setup Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

# Now you can import models and use Django ORM
from students.models import Student, Course, Instructor
from django.contrib.auth import get_user_model

User = get_user_model()


def main():
    # create users
    User.objects.create_superuser(
        username="admin",
        email="admin@email.com",
        password="admin123",
    )

    student_list = [
        {"username": "rabin", "first_name": "Rabin", "last_name": "Dhamala"},
        {"username": "simran", "first_name": "Simran", "last_name": "Karki"},
        {"username": "rakesh", "first_name": "Rakesh", "last_name": "Shrestha"},
        {"username": "priyanka", "first_name": "Priyanka", "last_name": "Dhamala"},
    ]
    for user in student_list:
        user = User.objects.create_user(
            email=f"{user['username']}@email.com",
            username=user["username"],
            first_name=user["first_name"],
            last_name=user["last_name"],
        )
        user.set_password("test123")
        user.save()
        Student.objects.create(user=user, date_of_birth="2000-01-01")

    # create courses
    Course.objects.bulk_create(
        [
            Course(
                name="Python Programming",
                code="CS101",
                description="Introduction to Python",
            ),
            Course(
                name="Data Science",
                code="CS102",
                description="Data Science with Python",
            ),
            Course(
                name="Web Development",
                code="CS103",
                description="Web Development using Django",
            ),
        ]
    )

    # create instructors
    User.objects.bulk_create(
        [
            User(
                email="doleshwor@email.com",
                username="doleshwor",
                first_name="Doleshwor",
                last_name="Niraula",
            ),
            User(
                email="smriti@email.com",
                username="smriti",
                first_name="Smriti",
                last_name="Pouydal",
            ),
            User(
                email="neera@email.com",
                username="neera",
                first_name="Neera",
                last_name="Pradhan",
            ),
        ]
    )
    Instructor.objects.bulk_create(
        [
            Instructor(user=User.objects.get(username="doleshwor")),
            Instructor(user=User.objects.get(username="smriti")),
            Instructor(user=User.objects.get(username="neera")),
        ]
    )

    # create enrollments
    for student in Student.objects.all():

        def get_grade():
            return random.choice(["A", "B", "C", "D", "F"])

        def get_score():
            return random.uniform(60.0, 100.0)

        for code in ["CS101", "CS102", "CS103"]:
            student.enrollments.create(
                course=Course.objects.get(code=code),
                grade=get_grade(),
                score=get_score(),
            )


if __name__ == "__main__":
    main()
