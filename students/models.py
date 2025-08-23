from django.db import models
from common.models import BaseModel, MetaData

from django.contrib.auth import get_user_model
from students.validators import validate_score

User = get_user_model()


class Student(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student")
    date_of_birth = models.DateField(null=True, blank=True)
    metadata = models.ManyToManyField(MetaData, blank=True, related_name="students")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ["-created_at"]

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name


class Course(BaseModel):
    name = models.CharField(max_length=100, db_index=True)
    code = models.CharField(max_length=100, unique=True)  # code is indexed by default
    description = models.TextField()
    metadata = models.ManyToManyField(MetaData, blank=True, related_name="courses")

    def __str__(self):
        return str(self.code)

    class Meta:
        ordering = ["-created_at"]


class Enrollment(BaseModel):

    GRADE_CHOICES = [
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
        ("F", "F"),
        ("NA", "Not Applicable"),
    ]

    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="enrollments"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="enrollments", db_index=True
    )
    enrollment_date = models.DateField(auto_now_add=True, db_index=True)
    score = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[validate_score],
    )
    metadata = models.ManyToManyField(MetaData, blank=True, related_name="enrollments")
    grade = models.CharField(
        max_length=2, choices=GRADE_CHOICES, default="NA", blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "course"], name="unique_student_course"
            )
        ]
        ordering = ["-enrollment_date"]
        indexes = [
            models.Index(fields=["student", "course"]),
        ]

    # although  grade is a computed property, we keep
    # it in the model for historical reasons also, this makes it
    # much easier to query for students with a specific grade and
    # and to save the grade, we retrieve the grade via grade_score
    # so it is the responsibility of the application logic to set
    # the grade field consistent with the score field

    @property
    def grade_score(self):
        if self.score is None:
            return "NA"
        elif self.score >= 80:
            return "A"
        elif self.score >= 70:
            return "B"
        elif self.score >= 60:
            return "C"
        elif self.score >= 50:
            return "D"
        elif self.score > 40:
            return "E"
        else:
            return "F"

    def __str__(self):
        return f"{self.student} -> {self.course}"


class Instructor(BaseModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="instructor_profile"
    )
    courses = models.ManyToManyField(Course, blank=True, related_name="instructors")
    metadata = models.ManyToManyField(MetaData, blank=True, related_name="instructors")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ["-created_at"]

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name
