from django.urls import path

from . import views

app_name = "app2"
urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("introduction", views.introduction, name="introduction"),
    path("change-password", views.change_password, name="change_password"),
    path("create-user", views.create_user, name="create_user"),
    path("users/", views.users, name="users"),
    path(r'users/^edit_user/(?P<id>\d+)/$', views.edit_user, name='edit_user'),
    path("logout", views.logout_view, name="logout")
]