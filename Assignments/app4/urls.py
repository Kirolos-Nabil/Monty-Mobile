from django.urls import path

from . import views

app_name = "app4"
urlpatterns = [
    path("diffie-hellman", views.diffie_hellman, name="diffie_hellman"),
]