from django.contrib import admin
from django.urls import path, include
from students.views import dashboard


urlpatterns = [
    path("students/", include("students.urls")),
    path("users/", include("users.urls")),
    path("common/", include("common.urls")),
    path("admin/", admin.site.urls),
    path("", dashboard, name="dashboard"),
]
