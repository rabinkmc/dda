from django.contrib.auth import get_user_model
from students.models import Instructor, Student, Course, Enrollment
from django.urls import reverse
from common.tests import BaseTestCase

User = get_user_model()


class StudentTestCase(BaseTestCase):
    def test_student_list_view(self):
        Student.objects.create(user=self.user, date_of_birth="2000-01-01")
        self.client.force_login(self.user)
        url = reverse("students:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "students/student_list.html")

    def test_student_detail_view(self):
        student = Student.objects.create(user=self.user, date_of_birth="2000-01-01")
        self.client.force_login(self.user)
        url = reverse("students:detail", kwargs={"pk": student.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "students/student_detail.html")
        self.assertContains(response, student.first_name)
        self.assertContains(response, student.last_name)

    def test_student_create_view(self):
        self.client.force_login(self.admin)
        url = reverse("students:create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "students/student_form.html")
        data = {
            "date_of_birth": "2000-01-01",
            "first_name": "Amy",
            "last_name": "Smith",
            "email": "amysmith@email.com",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Student.objects.filter(user__email=data["email"]).exists())

    def test_student_delete_view(self):
        self.client.force_login(self.admin)
        student = Student.objects.create(user=self.user, date_of_birth="2000-01-01")
        url = reverse("students:delete", kwargs={"pk": student.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Student.objects.filter(pk=student.pk).exists())

    def test_student_update_view(self):
        """
        create a student and update their details
        """
        self.client.force_login(self.admin)
        student = Student.objects.create(user=self.user, date_of_birth="2000-01-01")
        url = reverse("students:update", kwargs={"pk": student.pk})
        data = {
            "date_of_birth": "2000-01-01",
            "first_name": "Amy",
            "last_name": "Smith",
            "email": "amysmith@email.com",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        student.refresh_from_db()
        self.assertTrue(
            Student.objects.filter(
                user__first_name="Amy",
                user__last_name="Smith",
                user__email="amysmith@email.com",
                date_of_birth="2000-01-01",
            ).exists()
        )


class CourseTestCase(BaseTestCase):
    def test_course_list_view(self):
        Course.objects.create(name="Math 101", code="MTH101", description="Basic Math")
        self.client.force_login(self.user)
        url = reverse("students:courses-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "students/course_list.html")

    def test_course_detail_view(self):
        course = Course.objects.create(
            name="Math 101", code="MTH101", description="Basic Math"
        )
        self.client.force_login(self.user)
        url = reverse("students:courses-detail", kwargs={"pk": course.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "students/course_detail.html")

    def test_course_create_view(self):
        self.client.force_login(self.admin)
        url = reverse("students:courses-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "students/course_form.html")
        data = {
            "name": "Physics 101",
            "code": "PHY101",
            "description": "Basic Physics",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Course.objects.filter(code=data["code"]).exists())

    def test_course_update_view(self):
        """
        create a course and update its details
        """
        self.client.force_login(self.admin)
        course = Course.objects.create(
            name="Chemistry 101", code="CHEM101", description="Basic Chemistry"
        )
        url = reverse("students:courses-update", kwargs={"pk": course.pk})
        data = {
            "name": "Advanced Chemistry",
            "code": "CHEM201",
            "description": "Advanced Chemistry Concepts",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        course.refresh_from_db()
        self.assertTrue(
            Course.objects.filter(
                name="Advanced Chemistry",
                code="CHEM201",
                description="Advanced Chemistry Concepts",
            ).exists()
        )

    def test_course_delete_view(self):
        """
        create a course and delete it
        """
        self.client.force_login(self.admin)
        course = Course.objects.create(
            name="Chemistry 101", code="CHEM101", description="Basic Chemistry"
        )
        url = reverse("students:courses-delete", kwargs={"pk": course.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Course.objects.filter(pk=course.pk).exists())


class InstructorTestCase(BaseTestCase):
    def test_instructor_list_view(self):
        user1 = User.objects.create(
            username="instructor1", email="instructor@email.com"
        )
        user2 = User.objects.create(
            username="instructor2", email="instructor2@email.com"
        )
        Instructor.objects.create(user=user1)
        Instructor.objects.create(user=user2)
        self.client.force_login(self.user)
        url = reverse("students:instructors-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "students/instructor_list.html")

    def test_instructor_detail_view(self):
        user = User.objects.create_user(username="instructor1", password="password123")
        self.client.force_login(user)
        instructor = Instructor.objects.create(
            user=user,
        )
        url = reverse("students:instructors-detail", kwargs={"pk": instructor.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "students/instructor_detail.html")

    def test_instructor_create_view(self):
        url = reverse("students:instructors-create")
        self.client.force_login(self.admin)
        math101 = Course.objects.create(
            name="Math 101", code="MTH101", description="Basic Math"
        )
        cs201 = Course.objects.create(
            name="CS 201", code="CS201", description="Intermediate Computer Science"
        )
        data = {
            "first_name": "rakesh",
            "last_name": "suman",
            "email": "rakesh@email.com",
            "courses": [math101.pk, cs201.pk],
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Instructor.objects.filter(user__email="rakesh@email.com").exists()
        )
        instructor = Instructor.objects.get()
        self.assertTrue(
            instructor.courses.filter(code__in=[math101.code, cs201.code]).exists()
        )

    def test_instructor_update_view(self):
        instructor = Instructor.objects.create(
            user=self.user,
        )
        url = reverse("students:instructors-update", kwargs={"pk": instructor.pk})
        self.client.force_login(self.admin)
        self.assertTrue(
            Instructor.objects.filter(user__email="john@email.com").exists()
        )
        math101 = Course.objects.create(
            name="Math 101", code="MTH101", description="Basic Math"
        )
        cs201 = Course.objects.create(
            name="CS 201", code="CS201", description="Intermediate Computer Science"
        )
        data = {
            "first_name": "rakesh",
            "last_name": "suman",
            "email": "rakesh@email.com",
            "courses": [math101.pk, cs201.pk],
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Instructor.objects.filter(user__email="rakesh@email.com").exists()
        )
        self.assertTrue(
            instructor.courses.filter(code__in=[math101.code, cs201.code]).exists()
        )

    def test_instructor_delete_view(self):
        instructor = Instructor.objects.create(
            user=self.user,
        )
        url = reverse("students:instructors-delete", kwargs={"pk": instructor.pk})
        self.client.force_login(self.admin)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Instructor.objects.filter(pk=instructor.pk).exists())


class EnrollmentTestCase(BaseTestCase):
    def test_enrollment_list_view(self):
        student = Student.objects.create(user=self.user, date_of_birth="2000-01-01")
        course = Course.objects.create(
            name="Math 101", code="MTH101", description="Basic Math"
        )
        Enrollment.objects.create(
            student=student, course=course, score=85.00, grade="A"
        )
        self.client.force_login(self.user)
        url = reverse("students:enrollments-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "students/enrollment_list.html")

    def test_enrollment_detail_view(self):
        student = Student.objects.create(user=self.user, date_of_birth="2000-01-01")
        course = Course.objects.create(
            name="Math 101", code="MTH101", description="Basic Math"
        )
        enrollment = Enrollment.objects.create(
            student=student, course=course, score=85.00, grade="A"
        )
        self.client.force_login(self.user)
        url = reverse("students:enrollments-detail", kwargs={"pk": enrollment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "students/enrollment_detail.html")

    def test_enrollment_create_view(self):
        self.client.force_login(self.admin)
        student = Student.objects.create(user=self.user, date_of_birth="2000-01-01")
        course = Course.objects.create(
            name="Math 101", code="MTH101", description="Basic Math"
        )
        url = reverse("students:enrollments-create")
        data = {
            "student": student.pk,
            "course": course.pk,
            "score": 85.00,
            "grade": "A",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            student.enrollments.filter(course=course, score=85.00, grade="A").exists()
        )

    def test_enrollment_update_view(self):
        self.client.force_login(self.admin)
        student = Student.objects.create(user=self.user, date_of_birth="2000-01-01")
        course = Course.objects.create(
            name="Math 101", code="MTH101", description="Basic Math"
        )
        enrollment = Enrollment.objects.create(
            student=student, course=course, score=85.00, grade="A"
        )
        url = reverse("students:enrollments-update", kwargs={"pk": enrollment.pk})
        data = {
            "student": student.pk,
            "course": course.pk,
            "score": 90.00,
            "grade": "A",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        enrollment.refresh_from_db()
        self.assertTrue(enrollment.score == 90.00 and enrollment.grade == "A")

    def test_enrollment_delete_view(self):
        self.client.force_login(self.admin)
        student = Student.objects.create(user=self.user, date_of_birth="2000-01-01")
        course = Course.objects.create(
            name="Math 101", code="MTH101", description="Basic Math"
        )
        enrollment = Enrollment.objects.create(
            student=student, course=course, score=85.00, grade="A"
        )
        url = reverse("students:enrollments-delete", kwargs={"pk": enrollment.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Enrollment.objects.filter(pk=enrollment.pk).exists())
