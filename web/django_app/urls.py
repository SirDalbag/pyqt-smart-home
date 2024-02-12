from django.urls import path
from django_app import views

urlpatterns = [
    path("", views.index, name="index"),
    path("update", views.update, name="update"),
    path("api/", views.api),
]
