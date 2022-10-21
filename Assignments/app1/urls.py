from django.urls import path

from . import views

app_name = "app1"
urlpatterns = [
    path("users_api/", views.users, name="users"),
]