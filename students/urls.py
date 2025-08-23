from django.urls import path
from . import views

app_name = "students"

urlpatterns = [
    # students
    path("", views.student_list, name="list"),
    path("<int:pk>/", views.student_detail, name="detail"),
    path("create/", views.student_create, name="create"),
    path("<int:pk>/update/", views.student_update, name="update"),
    path("<int:pk>/delete/", views.student_delete, name="delete"),
    # Courses
    path("courses/", views.course_list, name="courses-list"),
    path("courses/<int:pk>/", views.course_detail, name="courses-detail"),
    path("courses/create/", views.course_create, name="courses-create"),
    path(
        "courses/<int:pk>/update/",
        views.course_update,
        name="courses-update",
    ),
    path(
        "courses/<int:pk>/delete/",
        views.course_delete,
        name="courses-delete",
    ),
    # Instructors
    path("instructors/", views.instructor_list, name="instructors-list"),
    path(
        "instructors/<int:pk>/",
        views.instructor_detail,
        name="instructors-detail",
    ),
    path(
        "instructors/create/",
        views.instructor_create,
        name="instructors-create",
    ),
    path(
        "instructors/<int:pk>/update/",
        views.instructor_update,
        name="instructors-update",
    ),
    path(
        "instructors/<int:pk>/delete/",
        views.instructor_delete,
        name="instructors-delete",
    ),
    # Enrollments
    path("enrollments/", views.enrollment_list, name="enrollments-list"),
    path(
        "enrollments/<int:pk>/",
        views.enrollment_detail,
        name="enrollments-detail",
    ),
    path(
        "enrollments/create/",
        views.enrollment_create,
        name="enrollments-create",
    ),
    path(
        "enrollments/<int:pk>/update/",
        views.enrollment_update,
        name="enrollments-update",
    ),
    path(
        "enrollments/<int:pk>/delete/",
        views.enrollment_delete,
        name="enrollments-delete",
    ),
]
