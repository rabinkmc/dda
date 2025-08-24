from django.urls import path
from . import views

app_name = "common"

urlpatterns = [
    path("metadata/", views.metadata_list, name="metadata-list"),
    path("metadata/<int:pk>/", views.metadata_detail, name="metadata-detail"),
    path("metadata/create/", views.metadata_create, name="metadata-create"),
    path("metadata/<int:pk>/update/", views.metadata_update, name="metadata-update"),
    path("metadata/<int:pk>/delete/", views.metadata_delete, name="metadata-delete"),
]
