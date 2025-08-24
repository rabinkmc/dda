from django.contrib import admin
from django.urls import path, include
from students.views import dashboard
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("students/", include("students.urls")),
    path("users/", include("users.urls")),
    path("common/", include("common.urls")),
    path("admin/", admin.site.urls),
    path("", dashboard, name="dashboard"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = (
        [
            path("__debug__/", include(debug_toolbar.urls)),
        ]
        + urlpatterns
        + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
