from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("metadata/", views.metadata_list, name="metadata-lis"),
]
