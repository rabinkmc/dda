from django.contrib import admin
from students.models import Student, Course, Enrollment, Instructor


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "user", "date_of_birth")
    search_fields = ("first_name", "last_name", "user__username")
    list_filter = ("date_of_birth",)
    filter_horizontal = ("metadata",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("code", "description")
    search_fields = ("code",)
    filter_horizontal = ("metadata",)


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "user")
    search_fields = ("first_name", "last_name", "user__username")
    filter_horizontal = ("metadata",)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "enrollment_date", "grade", "score")
    list_filter = ("course", "enrollment_date")
    search_fields = ("student__first_name", "student__last_name", "course__code")
    filter_horizontal = ("metadata",)
