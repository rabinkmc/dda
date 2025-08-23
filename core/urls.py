from django.contrib import admin
from django.urls import path, include
from students.views import dashboard


urlpatterns = [
    path("admin/", admin.site.urls),
    path("students/", include("students.urls")),
    path("users/", include("users.urls")),
    path("", dashboard, name="dashboard"),
]
