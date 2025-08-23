from students.models import Enrollment, Student, Course
from django.utils import timezone
from django import forms
from common.forms import BaseModelForm
from django.contrib.auth import get_user_model


User = get_user_model()


class StudentForm(BaseModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    date_of_birth = forms.DateField(required=False)
    email = forms.EmailField(required=True)

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get("date_of_birth")
        if date_of_birth and date_of_birth > timezone.now().date():
            raise forms.ValidationError("Date of birth cannot be in the future.")
        return date_of_birth

    def clean_email(self):
        email = self.cleaned_data["email"]
        qs = User.objects.filter(email=email)
        if self.instance:
            qs.exclude(id=self.instance.user.id)
        if qs.exists():
            raise forms.ValidationError("The email already exists.")
        return email


class InstructorForm(BaseModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(required=True)
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        required=False,
    )

    def clean_email(self):
        email = self.cleaned_data["email"]
        qs = User.objects.filter(email=email)
        if self.instance:
            qs.exclude(id=self.instance.user.id)
        if qs.exists():
            raise forms.ValidationError("The email already exists.")
        return email


class CourseForm(BaseModelForm):
    name = forms.CharField(max_length=100)
    code = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)

    def clean_code(self):
        code = self.cleaned_data["code"]
        qs = Course.objects.filter(code=code)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise forms.ValidationError("The course code already exists.")
        return code


class EnrollmentForm(BaseModelForm):
    student = forms.ModelChoiceField(queryset=Student.objects.all(), required=True)
    course = forms.ModelChoiceField(queryset=Course.objects.all(), required=True)
    score = forms.DecimalField(max_digits=5, decimal_places=2, required=False)
    enrollment_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )

    def clean(self):
        cleaned_data = super().clean()
        student = cleaned_data["student"]
        course = cleaned_data["course"]

        qs = Enrollment.objects.filter(student=student, course=course)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise forms.ValidationError(
                "This student is already enrolled in this course."
            )
        return cleaned_data


class MetaDataForm(BaseModelForm):
    name = forms.CharField(max_length=100)
    value = forms.CharField(max_length=255)

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get("name") or not cleaned_data.get("value"):
            raise forms.ValidationError("Both name and value are required.")
        return cleaned_data
